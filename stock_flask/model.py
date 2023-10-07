from databases import db

class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    percent = db.Column(db.Float, nullable=False)
    current = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    market_capital = db.Column(db.Float, nullable=False)
    float_market_capital = db.Column(db.Float, nullable=False)
    turnover_rate = db.Column(db.Float, nullable=False)
    chg = db.Column(db.Float, nullable=False)
    volume_ratio = db.Column(db.Float, nullable=False)
    total_shares = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Stock {self.symbol}>'
