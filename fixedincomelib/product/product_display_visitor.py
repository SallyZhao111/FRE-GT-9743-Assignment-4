from __future__ import annotations
from atexit import register
from typing import Any, Dict, List, Tuple
import pandas as pd
from functools import singledispatchmethod
from fixedincomelib.product.product_interfaces import Product, ProductVisitor
from fixedincomelib.product.product_portfolio import ProductPortfolio
from fixedincomelib.product.linear_products import (
    ProductBulletCashflow,
    ProductFixedAccrued,
    ProductOvernightIndexCashflow,
    ProductRFRSwap,
)


class ProductDisplayVisitor(ProductVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.nvps_ = [] # Name–Value Pairs

    @singledispatchmethod
    def visit(self, product: Product):
        raise NotImplementedError(f"No visitor for {Product._product_type}")

    def display(self) -> pd.DataFrame:
        return pd.DataFrame(self.nvps_, columns=["Name", "Value"])

    # TODO: ProductBulletCashflow
    # @visit.register
    # def _(self, product: ProductBulletCashflow):
    #     # Clear previous rows if you want each display call to show only one product
    #     self.nvps_.clear()

    #     # Decide what to display (reasonable “knowledge-based” fields)
    #     self.nvps_.append(["Product Type", getattr(product, "_product_type", type(product).__name__)])
    #     self.nvps_.append(["Termination Date", product.termination_date])
    #     self.nvps_.append(["Payment Date", product.payment_date])
    #     self.nvps_.append(["Currency", product.currency_.code])
    #     self.nvps_.append(["Notional", product.notional_])
    #     self.nvps_.append(["Long/Short", product.long_or_short_.name])

    #     # Optionally return something; not required because qfDisplayProduct calls display()
    #     return self
    # TODO: ProductFixedAccrued

    # TODO: ProductOvernightIndexCashflow

    # TODO: ProductRFRSwap

    # TODO: ProductBulletCashflow
    @visit.register
    def _(self, product: ProductBulletCashflow):
        self.nvps_.clear()

        self.nvps_.append(["Product Type", getattr(product, "_product_type", type(product).__name__)])
        self.nvps_.append(["Termination Date", product.termination_date])
        self.nvps_.append(["Payment Date", product.payment_date])

        # Currency is a wrapper that contains QuantLib currency in `ccy`
        cur = product.currency_
        cur_str = cur.ccy.code() if hasattr(cur, "ccy") and hasattr(cur.ccy, "code") else str(cur)
        self.nvps_.append(["Currency", cur_str])

        self.nvps_.append(["Notional", product.notional_])
        self.nvps_.append(["Long/Short", product.long_or_short_.name if hasattr(product.long_or_short_, "name") else str(product.long_or_short_)])

        return self

    # TODO: ProductFixedAccrued
    @visit.register
    def _(self, product: ProductFixedAccrued):
        self.nvps_.clear()

        self.nvps_.append(["Product Type", getattr(product, "_product_type", type(product).__name__)])

        self.nvps_.append(["Effective Date", getattr(product, "effective_date", getattr(product, "first_date_", None))])
        self.nvps_.append(["Termination Date", getattr(product, "termination_date", getattr(product, "last_date_", None))])
        self.nvps_.append(["Payment Date", getattr(product, "payment_date", getattr(product, "paymnet_date_", None))])

        cur = getattr(product, "currency_", None)
        cur_str = cur.ccy.code() if cur is not None and hasattr(cur, "ccy") and hasattr(cur.ccy, "code") else (str(cur) if cur is not None else None)
        self.nvps_.append(["Currency", cur_str])

        self.nvps_.append(["Notional", getattr(product, "notional_", None)])
        # self.nvps_.append(["Accrual Basis", getattr(product, "accrual_basis_", None)])
        basis = getattr(product, "accrual_basis_", None)
        try:
            basis_str = basis.name() if basis is not None and hasattr(basis, "name") else (
                basis.__class__.__name__ if basis is not None else None
            )
        except Exception:
            basis_str = basis.__class__.__name__ if basis is not None else None
        self.nvps_.append(["Accrual Basis", basis_str])
        # self.nvps_.append(["Business Day Convention", getattr(product, "business_day_convention_", None)])
        # self.nvps_.append(["Holiday Convention", getattr(product, "holiday_convention_", None)])
        bdc = getattr(product, "business_day_convention_", None)
        bdc_str = getattr(bdc, "value_str_", None)
        self.nvps_.append(["Business Day Convention", bdc_str])

        hol = getattr(product, "holiday_convention_", None)
        hol_str = getattr(hol, "value_str_", None)
        self.nvps_.append(["Holiday Convention", hol_str])
        return self

    # TODO: ProductOvernightIndexCashflow
    @visit.register
    def _(self, product: ProductOvernightIndexCashflow):
        self.nvps_.clear()

        self.nvps_.append(["Product Type", getattr(product, "_product_type", type(product).__name__)])

        self.nvps_.append(["Effective Date", getattr(product, "effective_date", getattr(product, "first_date_", None))])
        self.nvps_.append(["Termination Date", getattr(product, "termination_date", getattr(product, "last_date_", None))])
        self.nvps_.append(["Payment Date", getattr(product, "payment_date", getattr(product, "paymnet_date_", None))])

        self.nvps_.append(["Overnight Index", getattr(product, "overnight_index_", getattr(product, "on_index_", None))])
        self.nvps_.append(["Notional", getattr(product, "notional_", None)])
        #self.nvps_.append(["Compounding Method", getattr(product, "compounding_method_", None)])
        cm = getattr(product, "compounding_method_", None)
        cm_str = cm.name if hasattr(cm, "name") else str(cm)
        self.nvps_.append(["Compounding Method", cm_str])
        self.nvps_.append(["Spread", getattr(product, "spread_", None)])

        return self

    # TODO: ProductRFRSwap
    @visit.register
    def _(self, product: ProductRFRSwap):
        self.nvps_.clear()

        self.nvps_.append(["Product Type", getattr(product, "_product_type", type(product).__name__)])

        self.nvps_.append(["Effective Date", getattr(product, "effective_date", getattr(product, "first_date_", None))])
        self.nvps_.append(["Termination Date", getattr(product, "termination_date", getattr(product, "last_date_", None))])
        self.nvps_.append(["Pay Offset", getattr(product, "pay_offset_", None)])

        self.nvps_.append(["RFR Index", getattr(product, "on_index_", None)])
        self.nvps_.append(["Fixed Rate", getattr(product, "fixed_rate_", None)])

        pr = getattr(product, "pay_or_rec_", None)
        pr_str = pr.name if hasattr(pr, "name") else str(pr)
        self.nvps_.append(["Pay/Receive", pr_str])

        self.nvps_.append(["Notional", getattr(product, "notional_", None)])
        self.nvps_.append(["Accrual Period", getattr(product, "accrual_peroid_", getattr(product, "accrual_period_", None))])
        #self.nvps_.append(["Accrual Basis", getattr(product, "accrual_basis_", None)])
        basis = getattr(product, "accrual_basis_", None)
        try:
            basis_str = basis.name() if basis is not None and hasattr(basis, "name") else (
                basis.__class__.__name__ if basis is not None else None
            )
        except Exception:
            basis_str = basis.__class__.__name__ if basis is not None else None
        self.nvps_.append(["Accrual Basis", basis_str])
        self.nvps_.append(["Floating Leg Accrual Period", getattr(product, "floating_leg_accrual_period_", None)])

        self.nvps_.append(["Business Day Convention", getattr(product, "business_day_convention_", None)])
        self.nvps_.append(["Holiday Convention", getattr(product, "holiday_convention_", None)])

        self.nvps_.append(["Spread", getattr(product, "spread_", None)])
        self.nvps_.append(["Compounding Method", getattr(product, "compounding_method_", None)])

        return self
