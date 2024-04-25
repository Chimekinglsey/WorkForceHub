# """ Celery Module """
# import json
# from django.conf import settings
# from celery import Celery, shared_task


# app = Celery('tasks', broker=settings.CELERY_BROKER_URL, 
#              backend=settings.CELERY_RESULT_BACKEND)
# # app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')
# autodiscover_tasks = True
# print(settings.CELERY_BROKER_URL)

# @app.task(max_retries=3)
# def add(x:int, y:int) -> int:
#     print('running add task')
#     if x < 0 or y < 0:
#         raise ValueError('Negative numbers are not allowed')
#     return x + y

# # print(app)
# # result = add.apply_async((4, -4), countdown=5, retry=True, retry_policy={
# #     'max_retries': 3,
# #     'interval_start': 0,
# #     'interval_step': 0.2,
# #     'interval_max': 0.2,
# # })
# # if result.ready():
# #     print(f"{result.retries=}")
# #     # s = add.s(4, 4)
# # print(f"{result.retries=}")
# # print(f"{result.status=}")

# # from functools import wraps
# # from time import time
# # from typing import Callable, Any

# # def retrial(retry:int = 0, delay:int = 0, timeout: int = 0, backoff:bool = False ) -> Callable:
# #     def decorator(func: Callable = None) -> Callable:
# #         @wraps(func)
# #         def wrapper(*args, **kwds) -> Any:
# #             timer = 0
# #             while timeout > timer if timeout else True and retry >= 1:
# #                 try:
# #                     return func(*args, **kwds)
# #                 except Exception:
# #                     if delay > timer:
# #                         if backoff:
# #                             delay *= 2
# #                         time.sleep(delay)
# #                 timer += 1
# #                 retry -= 1
# #             raise Exception(f"Failed to execute task after {timer} attempts")
# #         return wrapper
# #     return decorator
                        

# # from celery import group, shared_task, chain, chord


# # @app.task
# # def fetch_in_batches(db_batch):
# #     fetched_data = 'dataset'
# #     return fetched_data

# # @app.task
# # def process_records(db_records):
# #     processed_data = [json.dumps(data) for data in fetch_in_batches(db_records)]
# #     return processed_data

# # @app.task
# # def aggregate_result(processed_data_list):
# #     d_set = group(process_records.si(data) for data in processed_data_list)()
# #     return d_set.get()

# # if __name__ == '__main__':
# #     final_result = chain(fetch_in_batches(db_batch)| process_records(db_records) | aggregate_result(processed_data_list))