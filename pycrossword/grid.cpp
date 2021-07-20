#include "grid.h"
#include "cwexception.h"

Grid::Grid(int width, int height, const std::vector<int>& black) : m_width(width), m_height(height), m_size(width * height) {

    m_chars = std::string(m_size, WHITE);
    for (auto i = 0 ; i < black.size(); i += 2) {
        m_chars[black[i] * m_width + black[i+1]] = BLACK;
    }
    setupDefinitions();
    computeNeighboers();
}

char Grid::getChar(int row, int col) const {
    if (row < 0 || row >= m_height || col < 0 || col >= m_width)
        return '#';
    return m_chars[row*m_width+col];
}

void Grid::setupDefinitions () {
    m_numbers = std::vector<int>(m_size, -1);
    m_horizontal = std::vector<int>(m_size, -1);
    m_vertical = std::vector<int>(m_size, -1);

    int n = 1;
    for (int i = 0; i < m_height; ++i)          // loop through rows (y)
    {
        int offset = i*m_width;
        for (int j = 0; j < m_width; ++j) {     // loop through cols (x)
            if (m_chars[offset + j] == BLACK)
                continue;
            bool wordStart = false;
            if ((j == 0 || m_chars[offset + j - 1] == '#') && (j < m_width-1 && m_chars[offset + j+1] != BLACK)) {
                // this is the beginning of a horizontal word
                // find the length
                int k = j+2;
                m_horizontal[offset+j] = n;
                m_horizontal[offset+j+1] = n;
                while (k < m_width && m_chars[offset+k] != '#') {
                    m_horizontal[offset+k] = n;
                    k++;
                }
                across[n] = Definition(n, i, j, k-j, Direction::ACROSS, offset+j);
                wordStart = true;
            }

            if ((i == 0 || m_chars[offset + j - m_width] == '#') && (i < m_height-1 && m_chars[offset+m_width+j] != '#')) {
                // this is the beginning of a vertical word
                // find length
                int k = i+2;
                m_vertical[offset+j] = n;
                m_vertical[(i+1)*m_width+j] = n;
                while (k < m_height && m_chars[k*m_width + j] != '#') {
                    m_vertical[k*m_width+j] = n;
                    k++;
                }
                down[n] = Definition (n, i, j, k-i, Direction::DOWN, offset+j);
                wordStart = true;
            }
            if (wordStart) {
                // I have at least a definition, increment n
                m_numbers[offset+j] = n;
                n++;
            }
        }
    }
}

void Grid::computeNeighboers() {
    m_neighbors = std::vector<int>(m_size);

    int counter = 0;
    for (int i = 0; i < m_height; ++i) {
        for (int j = 0; j < m_width; ++j) {

            if (getChar(i, j) == BLACK) {
                m_neighbors[counter++] = -1;
            }
            else {
                int neighbors = 0;
                bool topLeft = getChar(i-1, j-1) != BLACK;
                bool top = getChar(i-1, j) != BLACK;
                bool topRight = getChar(i-1, j+1) != BLACK;
                bool bottomLeft = getChar(i+1, j-1) != BLACK;
                bool bottom = getChar(i+1, j) != BLACK;
                bool bottomRight = getChar(i+1, j+1) != BLACK;
                bool left = getChar(i, j-1) != BLACK;
                bool right = getChar(i, j+1) != BLACK;
                if (topLeft && (top || left)) neighbors++;
                if (topRight && (top || right)) neighbors++;
                if (bottomLeft && (bottom || left)) neighbors++;
                if (bottomRight && (bottom || right)) neighbors++;
                neighbors += (top ? 1 : 0);
                neighbors += (bottom ? 1 : 0);
                neighbors += (left ? 1 : 0);
                neighbors += (right ? 1 : 0);
                m_neighbors[counter++] = neighbors;
            }
        }
    }

}


const Definition* Grid::getAcrossDefAt(int row, int col) const {
    int h = m_horizontal[row * m_width + col];
    return h == -1 ? nullptr : &across.at(h);
}

const Definition* Grid::getDownDefAt(int row, int col) const {
    int v = m_vertical[row * m_width + col];
    return v == -1 ? nullptr : &down.at(v);
}