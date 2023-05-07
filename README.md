[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# Q_Select_Learning

$$
d_1=\sqrt{(p_{1s}-p_{1c_1})^2+\dots+(p_{ns}-p_{nc_1})^2}
$$
$$
\vdots
$$
$$
d_m=\sqrt{(p_{1s}-p_{1c_m})^2+\dots+(p_{ns}-p_{nc_m})^2}
$$
$$
E(x)=d_1x_1+d_2x_2+\dots+d_{m}x_{m}
$$
|変数|内容|
|-|-|
|$p_1$|パラメータ1 : レベル(仮)|
|$p_2$|パラメータ2 : 必要時間(仮)|
|$p_3$|パラメータ3 : 人気度(仮)|
|$\vdots$|$\vdots$|
|$p_n$|パラメータn|
|$\bm{S}$|観測点(学習者)の座標($p_{1s},p_{2s},...,p_{ns}$)|
|$\bm{C}_1$|教材1の座標($p_{1c_1},p_{2c_1},...,p_{nc_1}$)|
|$\vdots$|$\vdots$|
|$\bm{C}_m$|教材$m$の座標($p_{1c_m},p_{2c_m},...,p_{nc_m}$)|
|$k$|選択する教材の数|
|$d_m$|観測点$\bm{S}$から教材$m$の座標へのユークリッド距離|


$$
E(x)=\sum_{i=1}^{m}d_{i}x_{i}+\lambda  \left(
\sum_{i=1}^{m}x_{i}-k\right) ^2
$$