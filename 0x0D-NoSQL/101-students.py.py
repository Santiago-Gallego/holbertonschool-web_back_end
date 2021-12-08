#!/usr/bin/env python3
""" Module that holds top students
"""

import pymongo


def top_students(mongo_collection):
    """ Method that returns all students
        sorted by average score
    """
    score = mongo_collection.aggregate([
        {'$project':
            {'name': '$name', 'averageScore': {'$avg': '$topics.score'}}},
        {'$sort': {'averageScore': -1}}])
    return score