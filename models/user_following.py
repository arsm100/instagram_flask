from instagram import db

class UserFollowing(db.Model):
    __tablename__ = 'user_followings'

    id = db.Column(db.Integer, primary_key=True)
    idol_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False, index=True)
    fan_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False, index=True)
    approved = db.Column(db.Boolean, nullable=False, index=True, default=False)

    __table_args__ = (
        db.Index('ix_unique_idol_fan', 'idol_id', 'fan_id', unique=True),
    )

    def __init__(self, idol_id, fan_id, approved):
        self.idol_id = idol_id
        self.fan_id = fan_id
        self.approved = approved

