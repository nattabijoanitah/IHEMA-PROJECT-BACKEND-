from datetime import datetime

from app.extensions import db


class Giving(db.Model):
    __tablename__ = "giving"

    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(10), default="UGX")
    purpose = db.Column(db.String(50), default="Tithe")  # Tithe, Offering, Missions, Building
    payment_method = db.Column(db.String(20))  # Card, Bank, Mobile Money
    status = db.Column(db.String(20), default="pending")  # pending, paid, failed
    transaction_ref = db.Column(db.String(120), unique=True)  # reference from payment processor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "donor_name": self.donor_name,
            "email": self.email,
            "amount": float(self.amount),
            "currency": self.currency,
            "purpose": self.purpose,
            "payment_method": self.payment_method,
            "status": self.status,
            "transaction_ref": self.transaction_ref,
            "created_at": self.created_at.isoformat(),
        }