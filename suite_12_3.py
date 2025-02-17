import unittest

def skip_if_frozen(method):
    def wrapper(self, *args, **kwargs):
        if self.is_frozen:
            self.skipTest('Тесты в этом кейсе заморожены')
        else:
            return method(self, *args, **kwargs)
    return wrapper

class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name

class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in sorted(self.participants, key=lambda x: x.speed, reverse=True):
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)
        return finishers

class RunnerTest(unittest.TestCase):
    is_frozen = False

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.usain = Runner("Усэйн", 10)
        self.andrei = Runner("Андрей", 9)
        self.nick = Runner("Ник", 3)

    @classmethod
    def tearDownClass(cls):
        for result in cls.all_results.values():
            print({place: str(runner) for place, runner in result.items()})

    @skip_if_frozen
    def test_walk(self):
        runner = Runner("TestRunner")
        for _ in range(10):
            runner.walk()
        self.assertEqual(runner.distance, 50)

    @skip_if_frozen
    def test_run(self):
        runner = Runner("TestRunner")
        for _ in range(10):
            runner.run()
        self.assertEqual(runner.distance, 100)

    @skip_if_frozen
    def test_challenge(self):
        runner1 = Runner("Runner1")
        runner2 = Runner("Runner2")
        for _ in range(10):
            runner1.run()
            runner2.walk()
        self.assertNotEqual(runner1.distance, runner2.distance)

class TournamentTest(unittest.TestCase):
    is_frozen = True

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.usain = Runner("Усэйн", 10)
        self.andrei = Runner("Андрей", 9)
        self.nick = Runner("Ник", 3)

    @classmethod
    def tearDownClass(cls):
        for result in cls.all_results.values():
            print({place: str(runner) for place, runner in result.items()})

    @skip_if_frozen
    def test_usain_and_nick(self):
        tournament = Tournament(90, self.usain, self.nick)
        results = tournament.start()
        self.__class__.all_results['test_usain_and_nick'] = results
        self.assertTrue(results[max(results.keys())] == self.nick)

    @skip_if_frozen
    def test_andrei_and_nick(self):
        tournament = Tournament(90, self.andrei, self.nick)
        results = tournament.start()
        self.__class__.all_results['test_andrei_and_nick'] = results
        self.assertTrue(results[max(results.keys())] == self.nick)

    @skip_if_frozen
    def test_usain_andrei_and_nick(self):
        tournament = Tournament(90, self.usain, self.andrei, self.nick)
        results = tournament.start()
        self.__class__.all_results['test_usain_andrei_and_nick'] = results
        self.assertTrue(results[max(results.keys())] == self.nick)

    @skip_if_frozen
    def test_usain_and_andrei(self):
        tournament = Tournament(90, self.usain, self.andrei)
        results = tournament.start()
        self.__class__.all_results['test_usain_and_andrei'] = results
        self.assertTrue(results[1] == self.usain)
        self.assertTrue(results[2] == self.andrei)

    @skip_if_frozen
    def test_all_runners_same_speed(self):
        runner1 = Runner("Runner1", 5)
        runner2 = Runner("Runner2", 5)
        runner3 = Runner("Runner3", 5)
        tournament = Tournament(90, runner1, runner2, runner3)
        results = tournament.start()
        self.__class__.all_results['test_all_runners_same_speed'] = results
        self.assertTrue(results[1] == runner1 or results[1] == runner2 or results[1] == runner3)
        self.assertTrue(results[2] == runner1 or results[2] == runner2 or results[2] == runner3)
        self.assertTrue(results[3] == runner1 or results[3] == runner2 or results[3] == runner3)


if __name__ == '__main__':
    unittest.main(verbosity=1)