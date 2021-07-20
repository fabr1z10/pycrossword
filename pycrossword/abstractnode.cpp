#include "abstractnode.h"

#include <sstream>
#include <pybind11/pybind11.h>
#include "rand.h"
#include "params.h"
#include "treenode.h"

namespace py = pybind11;

int AbstractNode::g_id = 0;

CellInfo::CellInfo(char letter, int horc, int vc) : m_letter(letter), m_horCount(horc), m_vertCount(vc) {
    // a problem here is that we run the risk of always generating the same solution or
    // very similar solutions if we don't add a bit of randomness...
    // TODO make the random magnitude a configurable param
    //int rs = Helper.randomScore;
    int rs = Params::get().getRandomScore();
    m_score = horc + vc - (rs / 2) + Random::get().getUniform(0, rs);
}

bool CellInfo::operator<(const CellInfo &other) const {
    if (m_score == other.m_score)
        return false;
    return m_score < other.m_score;
}


AbstractNode::AbstractNode(const Grid& grid, const Dict &dict) : m_id(g_id++), m_dict(dict), m_grid(grid), m_parent(nullptr) {
    //py::print("CIao");
    //py::print("word count is " + std::to_string(dict.getWordCount()));
    m_width = grid.getWidth();
    m_height = grid.getHeight();
    m_size = grid.getSize();
    m_solution = grid.getChars();
    m_depth = 0;
    m_data = std::vector<std::set<CellInfo>>(m_size);

}


AbstractNode::AbstractNode(const AbstractNode &parent) : m_id(g_id++), m_dict(parent.m_dict), m_grid(parent.m_grid) {
    m_solution = parent.m_solution;
    m_data = parent.m_data;
    m_depth = parent.m_depth+1;
    m_width = m_grid.getWidth();
    m_height = m_grid.getHeight();
    int i=0;

}

bool AbstractNode::operator<(const AbstractNode &other) const {

    if (m_depth == other.m_depth)
        return false;
    return (other.m_depth < m_depth);


}


char AbstractNode::getChar(int row, int col) const {
    return m_solution[row * m_width + col];
}

void AbstractNode::updateData(int rowStart, int h, int colStart, int w) {
    for (int i = 0; i < h; ++i) {
        for (int j = 0; j < w; ++j) {
            int row = rowStart + i;
            int col = colStart + j;
            //System.out.println("Doing cell (" + row + ", " + col +")");
            char c = getChar(row, col);
            int index = row * m_width + col;
            m_data[index] = std::set<CellInfo>();
            //py::print(" # updating info at "+ std::to_string(index));
            if (c == WHITE) {
                //CellInfo cInfo;
                // is there a horizontal word passing in (i, j)?
                int hk = -1;
                int vk = -1;
                int hn = -1;
                int vn = -1;
                std::string hw;
                std::string vw;
                const Definition* hdef = m_grid.getAcrossDefAt(row, col);
                if (hdef != nullptr) {
                    //py::print("find across def at " + std::to_string(row) + ", " + std::to_string(col) +" :" + hdef->toString());
                    int k = hdef->offset;
                    hw = m_solution.substr(k, hdef->length);
                    //py::print("hw = " + hw);
                    hk = col - hdef->icol;;
                }
                const Definition* vdef = m_grid.getDownDefAt(row, col);
                if (vdef != nullptr) {
                    //py::print("find down def at " + std::to_string(row) + ", " + std::to_string(col) +" :" + vdef->toString());
                    int k = vdef->offset;
                    for (int l = 0; l < vdef->length; ++l) {
                        vw.push_back(m_solution[k + l * m_width]);
                    }
                    //py::print("vw = " + vw);
                    vk = row - vdef->irow;
                }
                for (char d = 'a'; d <= 'z'; ++d) {
                    if (!hw.empty()) {
                        hw[hk] = d;
                        hn = m_dict.getNWords(hw);
                        //py::print("pattern = " + hw + " " + std::to_string(hn));
                    }
                    if (!vw.empty()) {
                        vw[vk] = d;
                        vn = m_dict.getNWords(vw);
                        //py::print("pattern = " + vw + " " + std::to_string(vn));
                    }
                    // if hn == 0 or vn == 0 then, by putting character d in (i, j) we don't have any words left.
                    if (hn != 0 && vn != 0) {
                        //py::print("setting " + std::to_string(index) +": " + std::to_string(hn) + ", " + std::to_string(vn));
                        m_data[index].insert(CellInfo(d, hn, vn));
                    }
                }

            }
        }
    }
}

int AbstractNode::evaluate() {
    if (m_solution.find('.') == -1) {
        return 0;
    }
    // if there are no decisions left, then it's a fail
    if (m_decisions.empty()) {
        //System.out.println("No decisions left!");
        return 2;
    }

    return 1;
}

std::shared_ptr<AbstractNode> AbstractNode::getNextDecision() {
    Decision nextDec = m_decisions.top();
    m_decisions.pop();
    py::print(" # decision: " + nextDec.toString());
    //System.out.println("Next decision, cell (" + nextDec.row + ", " + nextDec.col +") = " +nextDec.letter);
    return std::make_shared<TreeNode>(*this, nextDec); // new TreeNode(this, nextDec);
}

void AbstractNode::setChar(int row, int col, char c) {
    m_solution[row * m_width + col] = c;
}

std::string AbstractNode::toString() const {
    int k = 0;
    std::stringstream buffer;
    for (int i = 0; i < m_height; ++i) {
        for (int j = 0; j < m_width; ++j) {
            buffer << m_solution[k++];
        }
        buffer << std::endl;
    }
    return buffer.str();
}