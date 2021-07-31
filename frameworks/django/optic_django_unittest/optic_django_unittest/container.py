from __future__ import annotations

from functools import reduce
from typing import List

from optic_django_middleware.container import BasicInteractionContainer


class TestResultInteractionContainer(object):
    """Stores all the http interactions from a Test Run, aggregated by Test Case"""

    def __init__(self):
        self.interactions_by_testcase = dict()

    def add(self, test_case_id, http_interaction_container):
        """
        Merge the http_interactions from a test case
        :param test_case_id: identifier for test case (This is usually the
            full name of the test method, including the module and class name)
        :param http_interaction_container: TestCaseInteractionContainer for this test case
        """
        existing_interaction_container = self.interactions_by_testcase.get(
            test_case_id,
            {'interaction': TestCaseInteractionContainer(), 'success': True}
        )
        existing_interaction_container['interaction'].merge(http_interaction_container)
        self.interactions_by_testcase[test_case_id] = existing_interaction_container

    def update_test_result_status(self, test_case_id, success):
        existing_interaction_container = self.interactions_by_testcase.get(
            test_case_id,
            {'interaction': TestCaseInteractionContainer(), 'success': True}
        )
        if existing_interaction_container is not None and existing_interaction_container['success'] is True:
            existing_interaction_container['success'] = success
        self.interactions_by_testcase[test_case_id] = existing_interaction_container

    def get_interaction_list(self, include_failure=False) -> List:
        interactions = self.interactions_by_testcase
        if include_failure is False:
            interactions = dict(filter(lambda interaction: interaction[1]['success'] is True, interactions.items()))
        return list(reduce((lambda a, b: a + b[1]['interaction'].http_interactions), interactions.items(), []))


class TestCaseInteractionContainer(BasicInteractionContainer):
    """Stores http interactions by API for a particular test case"""
    http_interactions: list

    def __init__(self, http_interactions: list = None):
        super().__init__()
        self.http_interactions = http_interactions or list()

    def on_interaction_captured(self, serialized_interaction):
        self.http_interactions.append(serialized_interaction)

    def merge(self, test_case_container: TestCaseInteractionContainer):
        """
        Merges the http interactions from another test case container in this object
        """
        self.http_interactions += test_case_container.http_interactions
