import os
import subprocess
import re 
import logging

class SkybeardNightlyBuilds:
    def __init__(self, directory='../beards'):
       self.logger = logging.getLogger(__name__)
       logging.basicConfig()
       self.logger.setLevel('DEBUG')
       try:
          os.walk(directory)
       except:
          self.logger.error('Could not access directory structure.')
          raise SystemExit
       sub_directories = [(x[0], x[2]) for x in os.walk(directory) if '/test' in x[0]]
       self.tests_to_run = []
       self._get_test_tuple(sub_directories)
       self.output = {}
       self.summary = ''

    def _get_test_tuple(self, directories):
        for element in directories:
            for test in element[1]:
                beard_name = re.findall(r'beards/([\w\d\_]+)/test', element[0])[0]
                self.tests_to_run.append((beard_name, os.path.join(element[0], test)))

    def run_tests(self):
        for test in self.tests_to_run:
           if test[0] not in self.output:
             self.output[test[0]] = {}
           self.logger.info('Running Test: %s', test[1])
           process = subprocess.Popen(['python', '{}'.format(test[1])], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
           output, err = process.communicate()
           test_name = re.findall(r'tests/([\w\d\_]+).py',test[1])[0]
           self.output[test[0]][test_name] = {}
           self.output[test[0]][test_name]['stderr'] = err
           self.output[test[0]][test_name]['stdout'] = output

if __name__=="__main__":
   x = SkybeardNightlyBuilds()
   x.run_tests()
   print(x.output)
