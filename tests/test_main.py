from numpy import allclose, nan
from regional import many
from neurofinder import match, shapes, centers


def test_match():
  a = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[10, 10], [10, 11], [11, 10], [11, 11]]])
  b = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[30, 30], [31, 30], [31, 31]]])
  assert match(a, b) == [0, 1]
  assert match(a, b, threshold=5) == [0, nan]


def test_match_flipped():
  a = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[10, 10], [10, 11], [11, 10], [11, 11]]])
  b = many([[[30, 30], [31, 30], [31, 31]], [[0, 0], [0, 1], [1, 0], [1, 1]]])
  assert match(a, b) == [1, 0]
  assert match(a, b, threshold=5) == [1, nan]


def test_similarity():
  a = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[10, 10], [10, 11], [11, 10], [11, 11]]])
  b = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[30, 30], [31, 30], [31, 31]]])
  assert centers(a, b, threshold=5) == (0.5, 0.5)


def test_similarity_no_threshold():
  a = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[10, 10], [10, 11], [11, 10], [11, 11]]])
  b = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[30, 30], [31, 30], [31, 31]]])
  assert centers(a, b) == (1.0, 1.0)


def test_similarity_perfect():
  a = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[10, 10], [10, 11], [11, 10], [11, 11]]])
  b = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[10, 10], [10, 11], [11, 10], [11, 11]]])
  assert centers(a, b) == (1.0, 1.0)


def test_similarity_perfect_flipped():
  a = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[10, 10], [10, 11], [11, 10], [11, 11]]])
  b = many([[[10, 10], [10, 11], [11, 10], [11, 11]], [[0, 0], [0, 1], [1, 0], [1, 1]]])
  assert centers(a, b) == (1.0, 1.0)


def test_overlap_too_few():
  a = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[10, 10], [10, 11], [11, 10], [11, 11]]])
  b = many([[[0, 0], [0, 1], [1, 0], [1, 1]], [[10, 10], [11, 11]]])
  assert shapes(a, b) == (0.75, 1.0)


def test_overlap_too_many():
  a = many([[[0, 0], [0, 1]], [[10, 10], [10, 11]]])
  b = many([[[0, 0], [0, 1]], [[10, 10], [10, 11], [11, 10], [11, 12]]])
  assert shapes(a, b) == (1.0, 0.75)


def test_overlap_perfect():
  a = many([[[0, 0], [0, 1]], [[10, 10], [10, 11]]])
  b = many([[[0, 0], [0, 1]], [[10, 10], [10, 11]]])
  assert shapes(a, b) == (1.0, 1.0)


def test_overlap_perfect_flipped():
  a = many([[[0, 0], [0, 1]], [[10, 10], [10, 11]]])
  b = many([[[10, 10], [10, 11]], [[0, 0], [0, 1]]])
  assert shapes(a, b) == (1.0, 1.0)