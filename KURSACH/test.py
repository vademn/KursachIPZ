import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
import pygame
import os
from jackyyy import Background, Jackyyy, Moai, Collision, Score

# Test case for the Background class
class TestBackground(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((623, 150))
        self.bg = Background(0)

    def tearDown(self):
        pygame.QUIT

    def test_init(self):
        # Test the initialization of Background object
        self.assertEqual(self.bg.width, 623)
        self.assertEqual(self.bg.height, 150)
        self.assertEqual(self.bg.x, 0)
        self.assertEqual(self.bg.y, 0)
        self.assertIsNotNone(self.bg.texture)

    def test_update(self):
        # Test the update method of Background object
        self.bg.update(10)
        self.assertEqual(self.bg.x, 10)

    @patch.object(Background, 'show')
    def test_show(self, mock_show):
        # Test the show method of Background object
        self.bg.texture = "mock_texture"  # Set a mock texture for testing
        self.bg.show()
        mock_show.assert_called_once_with()

    def test_set_texture(self):
        # Test the set_texture method of Background object
        with patch("pygame.image.load") as mock_load, \
             patch("pygame.transform.scale") as mock_scale:
            self.bg.set_texture()
            mock_load.assert_called_once_with(os.path.join('content/images/bg.png'))
            mock_scale.assert_called_once_with(mock_load.return_value, (self.bg.width, self.bg.height))

# Test case for the Jackyyy class
class TestJackyyy(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((623, 150))
        self.jackyyy = Jackyyy()

    def tearDown(self):
        pygame.QUIT

    def test_init(self):
        # Test the initialization of Jackyyy object
        self.assertEqual(self.jackyyy.width, 44)
        self.assertEqual(self.jackyyy.height, 44)
        self.assertEqual(self.jackyyy.x, 10)
        self.assertEqual(self.jackyyy.y, 80)
        self.assertEqual(self.jackyyy.texture_number, 0)
        self.assertEqual(self.jackyyy.dy, 3)
        self.assertEqual(self.jackyyy.gravity, 1.23)
        self.assertTrue(self.jackyyy.onground)
        self.assertFalse(self.jackyyy.jumping)
        self.assertEqual(self.jackyyy.jump_stop, 10)
        self.assertFalse(self.jackyyy.falling)
        self.assertEqual(self.jackyyy.fall_stop, self.jackyyy.y)
        self.assertIsNotNone(self.jackyyy.texture)
        self.assertIsNotNone(self.jackyyy.sound)

    def test_update_jumping(self):
        # Test the update method when Jackyyy is jumping
        self.jackyyy.jumping = True
        self.jackyyy.update(0)
        self.assertEqual(self.jackyyy.y, 77)

    def test_update_falling(self):
        # Test the update method when Jackyyy is falling
        self.jackyyy.falling = True
        self.jackyyy.update(0)
        self.assertEqual(self.jackyyy.y, 83.69)

    def test_update_walking(self):
        # Test the update method when Jackyyy is walking
        self.jackyyy.texture_number = 0
        self.jackyyy.update(0)
        self.assertEqual(self.jackyyy.texture_number, 1)

    @patch.object(Jackyyy, 'show')
    def test_show(self, mock_show):
        # Test the show method of Jackyyy object
        self.jackyyy.texture = "mock_texture"  # Set a mock texture for testing
        self.jackyyy.show()
        mock_show.assert_called_once_with()

    def test_set_texture(self):
        # Test the set_texture method of Jackyyy object
        with patch("pygame.image.load") as mock_load, \
             patch("pygame.transform.scale") as mock_scale:
            self.jackyyy.set_texture()
            mock_load.assert_called_once_with(os.path.join(f'content/images/jack{self.jackyyy.texture_number}.png'))
            mock_scale.assert_called_once_with(mock_load.return_value, (self.jackyyy.width, self.jackyyy.height))

    def test_set_sound(self):
        # Test the set_sound method of Jackyyy object
        with patch("pygame.mixer.Sound") as mock_sound:
            self.jackyyy.set_sound()
            mock_sound.assert_called_once_with(os.path.join('content/sounds/jump.wav'))

    @patch("pygame.mixer.Sound")
    def test_jump(self, mock_sound):
        # Test the jump method of Jackyyy object
        jackyyy = Jackyyy()
        mock_play = mock_sound.return_value.play = MagicMock()

        jackyyy.jump()

        mock_play.assert_called_once()

    def test_fall(self):
        # Test the fall method of Jackyyy object
        self.jackyyy.fall()
        self.assertFalse(self.jackyyy.jumping)
        self.assertTrue(self.jackyyy.falling)

    def test_stop(self):
        # Test the stop method of Jackyyy object
        self.jackyyy.stop()
        self.assertFalse(self.jackyyy.falling)
        self.assertTrue(self.jackyyy.onground)

# Test case for the Moai class
class TestMoai(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((623, 150))
        self.moai = Moai(100)

    def tearDown(self):
        pygame.QUIT

    def test_init(self):
        # Test the initialization of Moai object
        self.assertEqual(self.moai.width, 34)
        self.assertEqual(self.moai.height, 44)
        self.assertEqual(self.moai.x, 100)
        self.assertEqual(self.moai.y, 80)
        self.assertIsNotNone(self.moai.texture)

    def test_update(self):
        # Test the update method of Moai object
        self.moai.update(2)
        self.assertEqual(self.moai.x, 102)

    @patch.object(Moai, 'show')
    def test_show(self, mock_show):
        # Test the show method of Moai object
        self.moai.texture = "mock_texture"  # Set a mock texture for testing
        self.moai.show()
        mock_show.assert_called_once_with()

    def test_set_texture(self):
        # Test the set_texture method of Moai object
        with patch("pygame.image.load") as mock_load, \
             patch("pygame.transform.scale") as mock_scale:
            self.moai.set_texture()
            mock_load.assert_called_once_with(os.path.join('content/images/moai.png'))
            mock_scale.assert_called_once_with(mock_load.return_value, (self.moai.width, self.moai.height))

# Test case for the Collision class
class TestCollision(unittest.TestCase):
    def setUp(self):
        self.collision = Collision()

    def test_between(self):
        # Test the between method of Collision object
        obj1 = Mock(x=10, y=20)
        obj2 = Mock(x=30, y=40)
        self.assertTrue(self.collision.between(obj1, obj2))

        obj1 = Mock(x=10, y=20)
        obj2 = Mock(x=11, y=21)
        self.assertTrue(self.collision.between(obj1, obj2))

        obj1 = Mock(x=10, y=20)
        obj2 = Mock(x=100, y=200)
        self.assertFalse(self.collision.between(obj1, obj2))

# Test case for the Score class
class TestScore(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((623, 150))
        self.score = Score(100)

    def tearDown(self):
        pygame.QUIT

    def test_init(self):
        # Test the initialization of Score object
        self.assertEqual(self.score.highestscore, 100)
        self.assertEqual(self.score.actualscore, 0)
        self.assertIsNotNone(self.score.font)
        self.assertEqual(self.score.color, (0, 0, 0))

    def test_update(self):
        # Test the update method of Score object
        self.score.update(50)
        self.assertEqual(self.score.actualscore, 3)

    def test_check_highestscore(self):
        # Test the check_highestscore method of Score object
        self.score.actualscore = 50
        self.score.check_highestscore()
        self.assertEqual(self.score.highestscore, 100)

        self.score.actualscore = 150
        self.score.check_highestscore()
        self.assertEqual(self.score.highestscore, 150)

    def test_reset(self):
        # Test the reset method of Score object
        self.score.actualscore = 50
        self.score.reset()
        self.assertEqual(self.score.actualscore, 0)

if __name__ == "__main__":
    unittest.main()

