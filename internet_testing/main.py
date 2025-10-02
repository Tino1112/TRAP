import speedtest
import logging
from time import sleep
from database.database import Database
from internet_testing.tables import Tests

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger(__name__)

class SpeedTest:
    def __init__(self):
        self.database = Database('pstg', logger)
        self.time_delay = 180

        self.workflow()

    def test_internet_speed(self):
        st = speedtest.Speedtest()
        st.get_best_server()

        logger.info(f'Testing download speed')
        download_speed = round(st.download() / 1_000_000, 2)  # Convert from bits/s to Mbps
        logger.info(f'Testing upload speed')
        upload_speed = round(st.upload() / 1_000_000, 2)  # Convert from bits/s to Mbps
        logger.info(f'Testing ping speed')
        ping = round(st.results.ping, 2)

        data_dict = {'download_speed': download_speed, 'upload_speed': upload_speed, 'ping': ping}
        print(data_dict)
        return data_dict

    def workflow(self):
        with self.database.start_session() as pstg_session:
            while True:
                try:
                    logger.info(f'Starting testing internet speed')
                    data = self.test_internet_speed()
                    self.database.insert_data(data, Tests, pstg_session)
                    logger.info('Data inserted')
                    sleep(self.time_delay)
                except speedtest.ConfigRetrievalError:
                    continue


if __name__ == '__main__':
    st = SpeedTest()
