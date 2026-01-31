#!/usr/bin/env python3
"""
Fix TikZ diagrams by adding back text labels using absolute positioning
instead of relative positioning to avoid overlap.
"""

import re

# Chapter 5: CNN
ch5_fix = r'''% Input feature map (5x5)
\node[font=\small] at (2.5, 3.2) {Input};
\foreach \i in {0,...,4} {
    \foreach \j in {0,...,4} {
        \node[cell] (in\i\j) at (\j*0.6, -\i*0.6) {};
    }
}

% Highlight receptive field for first output
\foreach \i in {0,1,2} {
    \foreach \j in {0,1,2} {
        \node[kernel] at (\j*0.6, -\i*0.6) {};
    }
}

% 3x3 Kernel
\node[font=\small] at (5, 0.5) {$3 \times 3$ Kernel};
\foreach \i in {0,1,2} {
    \foreach \j in {0,1,2} {
        \node[kernel] (k\i\j) at (4.5+\j*0.6, -\i*0.6) {$w$};
    }
}

% Output feature map (3x3)
\node[font=\small] at (8.5, 0.5) {Output};
\foreach \i in {0,1,2} {
    \foreach \j in {0,1,2} {
        \node[output] (out\i\j) at (7.5+\j*0.8, -\i*0.8) {};
    }
}

% Highlight first output
\node[output, fill=green!50] at (7.5, 0) {$y_{11}$};

% Arrows showing receptive field
\draw[arrow, red, thick] (1.2, -1.2) -- (4.2, -0.5);
\draw[arrow, blue, thick] (5.7, -0.5) -- (7.3, -0.2);'''

print("Chapter 5 CNN fix:")
print(ch5_fix)
print("\n" + "="*80 + "\n")

# Chapter 6: RNN
ch6_rnn_fix = r'''% Hidden states
\node[node] (h0) at (0,0) {$\vh_0$};
\node[node] (h1) at (3,0) {$\vh_1$};
\node[node] (h2) at (6,0) {$\vh_2$};
\node[node] (h3) at (9,0) {$\vh_3$};

% Time step labels at fixed coordinates
\node[font=\small] at (0, 2.5) {$t=0$};
\node[font=\small] at (3, 2.5) {$t=1$};
\node[font=\small] at (6, 2.5) {$t=2$};
\node[font=\small] at (9, 2.5) {$t=3$};

% Inputs
\node[input] (x1) at (3,1.5) {$\vx_1$};
\node[input] (x2) at (6,1.5) {$\vx_2$};
\node[input] (x3) at (9,1.5) {$\vx_3$};

% Outputs
\node[input] (y1) at (3,-1.5) {$\vy_1$};
\node[input] (y2) at (6,-1.5) {$\vy_2$};
\node[input] (y3) at (9,-1.5) {$\vy_3$};

% Recurrent connections (horizontal) with weight labels
\draw[recurrent] (h0) -- (h1) node[midway, above, font=\tiny] {$\mW_{hh}$};
\draw[recurrent] (h1) -- (h2) node[midway, above, font=\tiny] {$\mW_{hh}$};
\draw[recurrent] (h2) -- (h3) node[midway, above, font=\tiny] {$\mW_{hh}$};

% Input connections (vertical)
\draw[arrow, blue!70] (x1) -- (h1) node[midway, right, font=\tiny] {$\mW_{xh}$};
\draw[arrow, blue!70] (x2) -- (h2);
\draw[arrow, blue!70] (x3) -- (h3);

% Output connections (vertical)
\draw[arrow] (h1) -- (y1) node[midway, right, font=\tiny] {$\mW_{hy}$};
\draw[arrow] (h2) -- (y2);
\draw[arrow] (h3) -- (y3);'''

print("Chapter 6 RNN fix:")
print(ch6_rnn_fix)
print("\n" + "="*80 + "\n")

# Chapter 6: LSTM
ch6_lstm_fix = r'''% Inputs at top
\node[state] (input) at (0,4) {$[\vh_{t-1}, \vx_t]$};

% Four gates with labels at fixed coordinates
\node[gate] (forget) at (-3,2.5) {$\sigma$};
\node[font=\footnotesize] at (-3, 3.5) {Forget};

\node[gate] (input_gate) at (-1,2.5) {$\sigma$};
\node[font=\footnotesize] at (-1, 3.5) {Input};

\node[gate] (candidate) at (1,2.5) {$\tanh$};
\node[font=\footnotesize] at (1, 3.5) {Candidate};

\node[gate] (output_gate) at (3,2.5) {$\sigma$};
\node[font=\footnotesize] at (3, 3.5) {Output};

% Cell state flow (horizontal)
\node[state] (c_prev) at (-4,0) {$\mathbf{c}_{t-1}$};
\node[state] (c_curr) at (2,0) {$\mathbf{c}_t$};

% Operations
\node[operation] (mult1) at (-3,0) {$\odot$};
\node[operation] (mult2) at (1,0) {$\odot$};
\node[operation] (add) at (-1,0) {$+$};
\node[operation] (tanh_c) at (2,-1.5) {$\tanh$};
\node[operation] (mult3) at (3,-1.5) {$\odot$};

% Hidden state output
\node[state] (h_out) at (3,-3) {$\vh_t$};

% Connections from input to gates
\draw[arrow] (input) -- (-3,3.2);
\draw[arrow] (input) -- (-1,3.2);
\draw[arrow] (input) -- (1,3.2);
\draw[arrow] (input) -- (3,3.2);

% Gate outputs to operations
\draw[arrow] (forget) -- (mult1);
\draw[arrow] (input_gate) -- (mult2);
\draw[arrow] (candidate) -- (mult2);
\draw[arrow] (output_gate) -- (mult3);

% Cell state flow (the "highway")
\draw[cell_flow] (c_prev) -- (mult1);
\draw[cell_flow] (mult1) -- (add);
\draw[cell_flow] (add) -- (c_curr);
\draw[arrow] (mult2) -- (add);

% Cell to output
\draw[arrow] (c_curr) -- (tanh_c);
\draw[arrow] (tanh_c) -- (mult3);
\draw[arrow] (mult3) -- (h_out);'''

print("Chapter 6 LSTM fix:")
print(ch6_lstm_fix)
