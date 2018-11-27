from instagram import db

class FollowerRequest(db.Model):
    __tablename__ = 'follower_requests'

    id = db.Column(db.Integer, primary_key=True)
    idol_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False, index=True)
    fan_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False, index=True)

    __table_args__ = (
        db.Index('ix_unique_idol_fan_request', 'idol_id', 'fan_id', unique=True),
    )

    def __init__(self, donor_id, image_id, amount):
        self.idol_id = donor_id
        self.fan_id = image_id
