#include <iostream>
#include <vector>

class MatrixMultiplier {
public:
    static std::vector<std::vector<int>> multiply(const std::vector<std::vector<int>>& mat1, const std::vector<std::vector<int>>& mat2) {
        int r1 = mat1.size();
        int c1 = mat1[0].size();
        int c2 = mat2[0].size();
        std::vector<std::vector<int>> product(r1, std::vector<int>(c2, 0));

        for (int row = 0; row < r1; ++row) {
            for (int col = 0; col < c2; ++col) {
                for (int mid = 0; mid < c1; ++mid) {
                    product[row][col] += mat1[row][mid] * mat2[mid][col];
                }
            }
        }
        return product;
    }
};
