from datetime import datetime

import mongoengine


class Lines(mongoengine.Document):

    task_id = mongoengine.StringField(required=True)  # task id
    result = mongoengine.DictField(required=False)  # result
    executed = mongoengine.DateTimeField(default=datetime.now())

    def __repr__(self):
        return "<Task id '{}'\
        and result'{}'>".format(
            self.task_id, self.result
        )

    meta = {
        "indexes": [
            {
                "fields": ("task_id",),
                "unique": True,
            }
        ],
    }
