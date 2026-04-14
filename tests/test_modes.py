import unittest
import os
import shutil
import sys
import subprocess

class TestModes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set paths
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        cls.strat_dir = os.path.join(cls.base_dir, 'strategies')
        cls.test_strat_dir = os.path.join(cls.base_dir, 'test_strategies')
        
        if not os.path.exists(cls.test_strat_dir):
            os.makedirs(cls.test_strat_dir)

    def run_main(self, args):
        cmd = [sys.executable, os.path.join(self.base_dir, 'src', 'main.py')] + args
        # Run from base dir to ensure paths resolve
        return subprocess.run(cmd, capture_output=True, text=True, cwd=self.base_dir)

    def test_generate_mode(self):
        # Clean up existing test strats if any
        if os.path.exists(self.strat_dir):
            # We use the default strat dir for the test
            result = self.run_main(['--mode', 'generate', '--count', '3'])
            self.assertEqual(result.returncode, 0)
            
            # Check if files were created
            strats = [f for f in os.listdir(self.strat_dir) if f.startswith('random_strategy_')]
            self.assertGreaterEqual(len(strats), 3)

    def test_evaluate_mode_priority(self):
        result = self.run_main(['--mode', 'evaluate', '--games', '2', '--ai', 'priority'])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Evaluating", result.stdout)
        self.assertIn("Avg Score", result.stdout)

    def test_evaluate_mode_expectimax(self):
        # Only 1 game for speed
        result = self.run_main(['--mode', 'evaluate', '--games', '1', '--ai', 'expectimax'])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Expectimax", result.stdout)

    def test_evaluate_mode_mcts(self):
        result = self.run_main(['--mode', 'evaluate', '--games', '1', '--ai', 'mcts'])
        self.assertEqual(result.returncode, 0)
        self.assertIn("MCTS", result.stdout)

if __name__ == '__main__':
    unittest.main()
