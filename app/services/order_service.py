"""
سرویس مدیریت سفارشات
"""
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import select, func, desc, and_

from app.core.logger import logger
from app.models.database import db
from app.models.order import Order


class OrderService:
    """CRUD سفارشات"""

    # =========================================================
    # ساخت
    # =========================================================
    def create(self, data: dict) -> Optional[Order]:
        """
        ساخت سفارش جدید

        داده مورد نیاز:
        - caller_phone, order_phone
        - address
        - items (لیست)
        - total_price
        - transcript (اختیاری)
        """
        try:
            with db.get_session() as session:
                # تولید کد سفارش یکتا
                order_code = self._generate_order_code(session)

                order = Order(
                    order_code=order_code,
                    session_id=data.get("session_id"),
                    caller_phone=data.get("caller_phone", ""),
                    order_phone=data.get("order_phone", ""),
                    is_same_as_caller=bool(data.get("is_same_as_caller", True)),
                    customer_name=data.get("customer_name") or None,
                    address=data.get("address", ""),
                    items=data.get("items", []),
                    items_count=len(data.get("items", [])),
                    total_price=int(data.get("total_price", 0)),
                    status=data.get("status", "pending"),
                    duration_seconds=int(data.get("duration_seconds", 0)),
                    transcript=data.get("transcript"),
                    notes=data.get("notes"),
                )
                session.add(order)
                session.commit()
                session.refresh(order)
                session.expunge(order)

                logger.info(
                    f"سفارش ساخته شد: {order.order_code} | "
                    f"{order.total_price:,} تومان"
                )
                return order

        except Exception as e:
            logger.exception(f"خطا در ساخت سفارش: {e}")
            return None

    def _generate_order_code(self, session) -> str:
        """تولید کد سفارش مثل ORD-20250928-0001"""
        today = datetime.now().strftime("%Y%m%d")
        prefix = f"ORD-{today}-"

        stmt = select(func.count(Order.id)).where(
            Order.order_code.like(f"{prefix}%")
        )
        count = (session.scalar(stmt) or 0) + 1
        return f"{prefix}{count:04d}"

    # =========================================================
    # خواندن
    # =========================================================
    def get_all(
        self,
        status: str | None = None,
        search: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int | None = None,
    ) -> List[Order]:
        """گرفتن لیست سفارشات با فیلتر"""
        with db.get_session() as session:
            stmt = select(Order)

            if status and status != "همه":
                stmt = stmt.where(Order.status == status)

            if search:
                like = f"%{search}%"
                stmt = stmt.where(
                    Order.caller_phone.ilike(like)
                    | Order.order_phone.ilike(like)
                    | Order.order_code.ilike(like)
                    | Order.address.ilike(like)
                )

            if date_from:
                stmt = stmt.where(Order.created_at >= date_from)
            if date_to:
                stmt = stmt.where(Order.created_at <= date_to)

            stmt = stmt.order_by(desc(Order.created_at))

            if limit:
                stmt = stmt.limit(limit)

            orders = list(session.scalars(stmt).all())
            for o in orders:
                session.expunge(o)
            return orders

    def get_by_id(self, order_id: int) -> Optional[Order]:
        with db.get_session() as session:
            o = session.get(Order, order_id)
            if o:
                session.expunge(o)
            return o

    def count(self, status: str | None = None) -> int:
        with db.get_session() as session:
            stmt = select(func.count(Order.id))
            if status:
                stmt = stmt.where(Order.status == status)
            return session.scalar(stmt) or 0

    def count_today(self) -> int:
        """تعداد سفارشات امروز"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        with db.get_session() as session:
            stmt = select(func.count(Order.id)).where(Order.created_at >= today)
            return session.scalar(stmt) or 0

    def sum_today(self) -> int:
        """مجموع فروش امروز"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        with db.get_session() as session:
            stmt = select(func.coalesce(func.sum(Order.total_price), 0)).where(
                Order.created_at >= today
            )
            return int(session.scalar(stmt) or 0)

    def sum_total(self) -> int:
        """مجموع کل فروش"""
        with db.get_session() as session:
            stmt = select(func.coalesce(func.sum(Order.total_price), 0))
            return int(session.scalar(stmt) or 0)

    # =========================================================
    # آمار برای گزارشات
    # =========================================================
    def stats_by_day(self, days: int = 7) -> list[dict]:
        """آمار فروش N روز اخیر"""
        result = []
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        with db.get_session() as session:
            for i in range(days - 1, -1, -1):
                day_start = today - timedelta(days=i)
                day_end = day_start + timedelta(days=1)

                stmt = select(
                    func.count(Order.id),
                    func.coalesce(func.sum(Order.total_price), 0),
                ).where(
                    and_(
                        Order.created_at >= day_start,
                        Order.created_at < day_end,
                    )
                )
                count, total = session.execute(stmt).one()
                result.append({
                    "date": day_start,
                    "label": day_start.strftime("%m/%d"),
                    "count": int(count or 0),
                    "total": int(total or 0),
                })
        return result

    def top_products(self, limit: int = 5) -> list[dict]:
        """پر فروش‌ترین محصولات"""
        product_stats: dict[str, dict] = {}

        with db.get_session() as session:
            stmt = select(Order.items)
            for items in session.scalars(stmt).all():
                if not items:
                    continue
                for item in items:
                    name = item.get("name", "نامشخص")
                    qty = int(item.get("quantity", 1))
                    price = int(item.get("price", 0))
                    if name not in product_stats:
                        product_stats[name] = {"name": name, "qty": 0, "revenue": 0}
                    product_stats[name]["qty"] += qty
                    product_stats[name]["revenue"] += qty * price

        sorted_products = sorted(
            product_stats.values(),
            key=lambda x: x["qty"],
            reverse=True,
        )
        return sorted_products[:limit]

    def stats_by_status(self) -> dict[str, int]:
        """تعداد سفارشات به تفکیک وضعیت"""
        with db.get_session() as session:
            stmt = select(Order.status, func.count(Order.id)).group_by(Order.status)
            return {status: int(count) for status, count in session.execute(stmt).all()}

    # =========================================================
    # آپدیت
    # =========================================================
    def update_status(self, order_id: int, status: str) -> bool:
        """آپدیت وضعیت سفارش"""
        try:
            with db.get_session() as session:
                order = session.get(Order, order_id)
                if order is None:
                    return False
                order.status = status
                session.commit()
                logger.info(f"وضعیت سفارش #{order_id} → {status}")
                return True
        except Exception as e:
            logger.error(f"خطا در آپدیت وضعیت: {e}")
            return False

    def update(self, order_id: int, data: dict) -> Optional[Order]:
        """آپدیت فیلدهای سفارش"""
        try:
            with db.get_session() as session:
                order = session.get(Order, order_id)
                if order is None:
                    return None

                allowed = ["status", "address", "notes", "customer_name"]
                for key in allowed:
                    if key in data:
                        setattr(order, key, data[key])

                session.commit()
                session.refresh(order)
                session.expunge(order)
                return order
        except Exception as e:
            logger.error(f"خطا در آپدیت سفارش: {e}")
            return None

    # =========================================================
    # حذف
    # =========================================================
    def delete(self, order_id: int) -> bool:
        try:
            with db.get_session() as session:
                order = session.get(Order, order_id)
                if order is None:
                    return False
                session.delete(order)
                session.commit()
                logger.info(f"سفارش #{order_id} حذف شد")
                return True
        except Exception as e:
            logger.error(f"خطا در حذف سفارش: {e}")
            return False


_order_service: OrderService | None = None


def get_order_service() -> OrderService:
    global _order_service
    if _order_service is None:
        _order_service = OrderService()
    return _order_service