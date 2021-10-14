import logging
import multiprocessing
from multiprocessing.context import Process
import time
import random


def work(item, count):
    name = multiprocessing.current_process().name
    logging.info(f'{name} started: {item}')

    for x in range(count):
        logging.info(f'{name}: {item} = {x}')
        time.sleep(1)
    logging.info(f'{name} finished')
    return item + ' is finished'


def proc_result(result):
    """
    Pulls the return from a process which was run
    :param result: The returned result
    """
    logging.info(f'Result = {result}')


def main():
    logging.info(f'Started ')

    max = 5
    # create a pool of processes
    pool = multiprocessing.Pool((max))
    results = []
    for x in range(max):
        item = 'Item' + str(x)
        count = random.randrange(1, 5) # how long the process will run for is unkn
        r = pool.apply_async(func=work, args=[item,count], callback=proc_result) # will do apply all at once
        results.append(r)

    # wait for results
    for r in results:
        r.wait()

    # pool.close() or pool.terminate
    pool.close()
    pool.join()
    logging.info('Finished')


logging.basicConfig(format='%(levelname)s - %(asctime)s; %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

if __name__ == "__main__":
    main()