import os
import subprocess
import re 
import logging

class SkybeardNightlyBuilds:
    def __init__(self, beard_directory='../beards', skb_core_tests='../tests'):
       self._beards_location = beard_directory
       self._skb_core_test_location = skb_core_tests
       self.logger = logging.getLogger(__name__)
       logging.basicConfig()
       self.logger.setLevel('DEBUG')
       try:
          os.walk(self._beards_location)
       except:
          self.logger.error('Could not access directory structure.')
          raise SystemExit
       self.beard_tests_to_run = []
       self.core_tests_to_run = []
       self._get_beard_test_tuple()
       self._get_skbcore_test_tuple()
       self.output = {}
       self.summary = ''

    def _get_beard_test_tuple(self):
        sub_directories = [(x[0], x[2]) for x in os.walk(self._beards_location) if '/test' in x[0]]
        for element in sub_directories:
            for test in element[1]:
                beard_name = re.findall(r'beards/([\w\d\_]+)/test', element[0])[0]
                self.tests_to_run.append((beard_name, os.path.join(element[0], test)))

    def _get_skbcore_test_tuple(self):
         skb_core_tests = [x[2] for x in os.walk(self._skb_core_test_location)][0]
         for test in skb_core_tests:
             self.core_tests_to_run.append(('skb-core', os.path.join(self._skb_core_test_location, test)))

    def run_beard_tests(self):
        for test in self.beard_tests_to_run:
           if test[0] not in self.output:
             self.output[test[0]] = {}
           self.logger.info('Running Test: %s', test[1])
           process = subprocess.Popen(['python', '{}'.format(test[1])], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
           output, err = process.communicate()
           test_name = re.findall(r'tests/([\w\d\_]+).py',test[1])[0]
           self.output[test[0]][test_name] = {}
           self.output[test[0]][test_name]['stderr'] = err
           self.output[test[0]][test_name]['stdout'] = output

    def run_skb_core_tests(self):
        for test in self.core_tests_to_run:
           if test[0] not in self.output:
             self.output[test[0]] = {}
           self.logger.info('Running Test: %s', test[1])
           process = subprocess.Popen(['python', '{}'.format(test[1])], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
           output, err = process.communicate()
           test_name = re.findall(r'tests/([\w\d\_]+).py',test[1])[0]
           self.output[test[0]][test_name] = {}
           self.output[test[0]][test_name]['stderr'] = err
           self.output[test[0]][test_name]['stdout'] = output
       
    def print_results(self):
         for key in self.output:
            for subkey in self.output[key]:
                print("{}: {}\n{}\n\n".format(key, subkey, str(self.output[key][subkey]['stderr'])))

 
if __name__=="__main__":
   x = SkybeardNightlyBuilds()
   x.run_skb_core_tests()
   x.print_results()
