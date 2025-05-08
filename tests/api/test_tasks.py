from tests.api.conftest import authed_session, task_data


class TestTasks:

    def test_delete_all_tasks(self, authed_session):
        all_tasks = self.test_get_all_tasks(authed_session)
        for task in all_tasks:
            authed_session.tasks_api.delete_task(task['id'])

    def test_get_all_tasks(self, authed_session):
        all_tasks = authed_session.tasks_api.get_all_tasks()
        return all_tasks.json()['tasks']

    def test_get_task(self, authed_session, task_data):
        task_id = self.test_successful_create_new_task(authed_session, task_data)['id']
        task = authed_session.tasks_api.get_task(task_id)
        task_json = task.json()

    def test_successful_create_new_task(self, authed_session, task_data):
        generated_task_data = task_data()
        created_task = authed_session.tasks_api.create_new_task(generated_task_data)
        created_task_json = created_task.json()
        return created_task_json


    def test_negative_create_new_task(self, authed_session):
        created_task = authed_session.tasks_api.create_new_task(None, 400)
        created_task_json = created_task.json()
        assert created_task_json['err'] == 'Task name invalid', f'Unexpected error message: {created_task_json['err']}'
        assert created_task_json['ECODE'] == 'INPUT_005', f'Unexpected error code: {created_task_json['ECODE']}'
        return created_task_json

    def test_successful_update_task(self, authed_session, task_data):
        task_id = self.test_successful_create_new_task(authed_session, task_data)['id']
        new_task_data = task_data()
        updated_task_json = authed_session.tasks_api.update_task(task_id, new_task_data).json()
        return updated_task_json

    def test_negative_update_task(self, authed_session, task_data):
        task_id = self.test_successful_create_new_task(authed_session, task_data)['id']
        new_task_data = None
        updated_task = authed_session.tasks_api.update_task(task_id, new_task_data)
        updated_task_json = updated_task.json()
        print(':::::::::::::', updated_task_json)

    def test_delete_task_by_id(self, authed_session, task_data):
        task_id = self.test_successful_create_new_task(authed_session, task_data)['id']
        delete_task_response = authed_session.tasks_api.delete_task(task_id)
        return delete_task_response