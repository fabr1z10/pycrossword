#include "treenode.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;
TreeNode::TreeNode(const AbstractNode &parent, const Decision &d) : AbstractNode(parent), m_decision(d) {

}

void TreeNode::init() {
    int row = m_decision.getRow();
    int col = m_decision.getCol();
    py::print("setting character at (" + std::to_string(row) + ", " + std::to_string(col) + ") to " + std::to_string(m_decision.getLetter()));
    setChar(row, col, m_decision.getLetter());

    // is there a horizontal word passing through (row, col)?
    const auto* hd = m_grid.getAcrossDefAt(row, col);
    const auto* vd = m_grid.getDownDefAt(row, col);

    if (hd != nullptr) {
        py::print(hd->toString());
        updateData (hd->irow, 1, hd->icol, hd->length);
    }
    if (vd != nullptr) {
        py::print(vd->toString());

        updateData (vd->irow, vd->length, vd->icol, 1);
    }

    // decisions
    // include only cells that border with
    int nMin = 1000;
    int irow = -1;
    int icol = -1;
    char let = '\0';
    for (int i = 0; i < m_height; ++i) {
        for (int j = 0; j < m_width; ++j) {
            char cc = getChar(i, j);
            if (cc != '.')
                continue;
            auto& c = m_data[i * m_width + j];
            //TreeSet<CellInfo> c = data.get(i * width + j);
            // IF IT EXISTS A CELL WITH NO POSSIBILITIES; JUST EXIT
            int n = c.size();
            if(n == 0)
            {
                py::print("mmah, no possibilities here." + std::to_string(i) + "," +std::to_string(j));
                return;
            }
            if (n > 0 && n < nMin) {
                irow = i;
                icol = j;
                nMin = n;
                //let = c.data.begin()->second.c;
            }
        }
    }
    if (irow == -1) {
        py::print("mmh, no possibilities here.");
        return;
    }
    //System.out.println("And the winner is (row = " + irow + ", col = " + icol + ") with n= " + nMin +")");
    const auto& c = m_data[irow * m_width + icol];
    for (const auto& stock : c) {
        m_decisions.push(Decision(irow, icol, stock.getLetter(), stock.getScore()));
    }


}