# coding=utf-8
class Solution(object):
    def findMedianSortedArrays(self, A, B):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: float
        """
        if len(A) > len(B):
            A, B = B, A
        m, n = len(A), len(B)
        s, e = 0, m
        if m + n == 0:
            return 0
        if m == 0:
            return (B[n / 2 - 1] + B[n / 2]) / 2.0 if n % 2 == 0 else B[n / 2]
        while True:
            i = (s + e + 1) / 2
            # 总长度的一半为(m + n + 1) / 2,不论奇偶数
            j = (m + n + 1) / 2 - i
            if i > 0 and A[i - 1] > B[j]:
                s, e = s, i - 1
            elif i < m and B[j - 1] > A[i]:
                s, e = i + 1, e
            else:
                if i == 0:
                    max_of_left = B[j - 1]
                elif j == 0:
                    max_of_left = A[i - 1]
                else:
                    max_of_left = max(A[i - 1], B[j - 1])
                if (m + n) % 2 == 1:
                    return max_of_left
                if i == m:
                    min_of_right = B[j]
                elif j == n:
                    min_of_right = A[i]
                else:
                    min_of_right = min(A[i], B[j])
                return (min_of_right + max_of_left) / 2.0


print Solution().findMedianSortedArrays([1, 3], [2])
