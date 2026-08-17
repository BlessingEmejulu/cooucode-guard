#include <iostream>
#include <vector>

class MatrixMultiplier {
public:
    static std::vector<std::vector<int>> multiply(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B) {
        int rowsA = A.size();
        int colsA = A[0].size();
        int colsB = B[0].size();
        std::vector<std::vector<int>> result(rowsA, std::vector<int>(colsB, 0));

        for (int i = 0; i < rowsA; ++i) {
            for (int j = 0; j < colsB; ++j) {
                for (int k = 0; k < colsA; ++k) {
                    result[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        return result;
    }
};
