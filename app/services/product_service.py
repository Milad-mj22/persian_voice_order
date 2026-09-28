"""
سرویس مدیریت محصولات
"""
from typing import List, Optional

from sqlalchemy import select, func, or_

from app.core.logger import logger
from app.models.database import db
from app.models.product import Product


class ProductService:
    """سرویس CRUD محصولات"""

    # =========================================================
    # خواندن
    # =========================================================
    def get_all(
        self,
        only_active: bool = False,
        search: str | None = None,
        category: str | None = None,
    ) -> List[Product]:
        """گرفتن همه محصولات با فیلترهای اختیاری"""
        with db.get_session() as session:
            stmt = select(Product)

            if only_active:
                stmt = stmt.where(Product.is_active == True)  # noqa: E712

            if search:
                like = f"%{search}%"
                stmt = stmt.where(
                    or_(
                        Product.name.ilike(like),
                        Product.description.ilike(like),
                    )
                )

            if category:
                stmt = stmt.where(Product.category == category)

            stmt = stmt.order_by(Product.display_order, Product.id)

            products = list(session.scalars(stmt).all())

            # جدا کردن از session (چون expire_on_commit=False)
            for p in products:
                session.expunge(p)

            return products

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """گرفتن یک محصول با ID"""
        with db.get_session() as session:
            product = session.get(Product, product_id)
            if product:
                session.expunge(product)
            return product

    def get_categories(self) -> List[str]:
        """گرفتن لیست همه دسته‌بندی‌ها"""
        with db.get_session() as session:
            stmt = select(Product.category).distinct().order_by(Product.category)
            return list(session.scalars(stmt).all())

    def count(self, only_active: bool = False) -> int:
        """تعداد کل محصولات"""
        with db.get_session() as session:
            stmt = select(func.count(Product.id))
            if only_active:
                stmt = stmt.where(Product.is_active == True)  # noqa: E712
            return session.scalar(stmt) or 0

    def get_featured(self) -> List[Product]:
        """محصولات پیشنهاد ویژه"""
        with db.get_session() as session:
            stmt = (
                select(Product)
                .where(Product.is_featured == True)  # noqa: E712
                .where(Product.is_active == True)  # noqa: E712
                .order_by(Product.display_order, Product.id)
            )
            products = list(session.scalars(stmt).all())
            for p in products:
                session.expunge(p)
            return products

    # =========================================================
    # نوشتن
    # =========================================================
    def create(self, data: dict) -> Optional[Product]:
        """ساخت محصول جدید"""
        try:
            with db.get_session() as session:
                product = Product(
                    name=data.get("name", "").strip(),
                    category=data.get("category", "").strip(),
                    price=int(data.get("price", 0)),
                    stock=int(data.get("stock", 0)),
                    description=data.get("description", "").strip() or None,
                    is_active=bool(data.get("is_active", True)),
                    is_featured=bool(data.get("is_featured", False)),
                    display_order=int(data.get("display_order", 0)),
                )
                session.add(product)
                session.commit()
                session.refresh(product)
                session.expunge(product)

                logger.info(f"محصول ساخته شد: #{product.id} {product.name}")
                return product

        except Exception as e:
            logger.error(f"خطا در ساخت محصول: {e}")
            return None

    def update(self, product_id: int, data: dict) -> Optional[Product]:
        """آپدیت محصول موجود"""
        try:
            with db.get_session() as session:
                product = session.get(Product, product_id)
                if product is None:
                    logger.warning(f"محصول #{product_id} پیدا نشد")
                    return None

                if "name" in data:
                    product.name = data["name"].strip()
                if "category" in data:
                    product.category = data["category"].strip()
                if "price" in data:
                    product.price = int(data["price"])
                if "stock" in data:
                    product.stock = int(data["stock"])
                if "description" in data:
                    product.description = data["description"].strip() or None
                if "is_active" in data:
                    product.is_active = bool(data["is_active"])
                if "is_featured" in data:
                    product.is_featured = bool(data["is_featured"])
                if "display_order" in data:
                    product.display_order = int(data["display_order"])

                session.commit()
                session.refresh(product)
                session.expunge(product)

                logger.info(f"محصول آپدیت شد: #{product.id} {product.name}")
                return product

        except Exception as e:
            logger.error(f"خطا در آپدیت محصول: {e}")
            return None

    def delete(self, product_id: int) -> bool:
        """حذف محصول"""
        try:
            with db.get_session() as session:
                product = session.get(Product, product_id)
                if product is None:
                    return False
                session.delete(product)
                session.commit()
                logger.info(f"محصول #{product_id} حذف شد")
                return True

        except Exception as e:
            logger.error(f"خطا در حذف محصول: {e}")
            return False

    def update_stock(self, product_id: int, new_stock: int) -> bool:
        """آپدیت موجودی محصول"""
        try:
            with db.get_session() as session:
                product = session.get(Product, product_id)
                if product is None:
                    return False
                product.stock = max(0, int(new_stock))
                session.commit()
                return True

        except Exception as e:
            logger.error(f"خطا در آپدیت موجودی: {e}")
            return False

    # =========================================================
    # Seed Data (اطلاعات نمونه)
    # =========================================================
    def seed_default_products(self) -> int:
        """اگر دیتابیس خالی بود، چند محصول نمونه اضافه کن"""
        if self.count() > 0:
            return 0

        samples = [
            {"name": "پیتزا مخصوص", "category": "پیتزا", "price": 185000,
             "stock": 20, "description": "پیتزا با پنیر فراوان و ژامبون",
             "is_featured": True, "display_order": 1},
            {"name": "پیتزا پپرونی", "category": "پیتزا", "price": 210000,
             "stock": 15, "description": "پیتزا با پپرونی تند",
             "display_order": 2},
            {"name": "پیتزا سبزیجات", "category": "پیتزا", "price": 165000,
             "stock": 10, "description": "پیتزا با سبزیجات تازه",
             "display_order": 3},
            {"name": "برگر دوبل", "category": "برگر", "price": 220000,
             "stock": 12, "description": "دو لایه گوشت گریل شده",
             "is_featured": True, "display_order": 4},
            {"name": "چیزبرگر", "category": "برگر", "price": 155000,
             "stock": 18, "description": "برگر با پنیر چدار",
             "display_order": 5},
            {"name": "ساندویچ فلافل", "category": "ساندویچ", "price": 95000,
             "stock": 25, "description": "ساندویچ فلافل با سس مخصوص",
             "display_order": 6},
            {"name": "نوشابه کوکاکولا", "category": "نوشیدنی", "price": 25000,
             "stock": 50, "description": "نوشابه خنک",
             "display_order": 7},
            {"name": "دوغ آبعلی", "category": "نوشیدنی", "price": 20000,
             "stock": 40, "description": "دوغ سنتی",
             "display_order": 8},
            {"name": "سیب‌زمینی سرخ‌کرده", "category": "پیش‌غذا", "price": 75000,
             "stock": 30, "description": "سیب‌زمینی تازه با سس",
             "display_order": 9},
            {"name": "سالاد سزار", "category": "پیش‌غذا", "price": 85000,
             "stock": 15, "description": "سالاد با سس سزار و مرغ گریل",
             "display_order": 10},
        ]

        created = 0
        for sample in samples:
            if self.create(sample):
                created += 1

        logger.info(f"{created} محصول نمونه اضافه شد")
        return created


# =========================================================
# Singleton
# =========================================================
_product_service: ProductService | None = None


def get_product_service() -> ProductService:
    global _product_service
    if _product_service is None:
        _product_service = ProductService()
    return _product_service