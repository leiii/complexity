表示学习已成为学习文本和图形等符号数据的宝贵方法。 然而，现有技术的嵌入方法通常不考虑潜在的分层结构，其是许多复杂符号数据集的特征。 在这项工作中，我们介绍了一种新方法，通过将符号数据嵌入到双曲空间中来学习它们的层次表示 - 或者更准确地说，将其嵌入到n维庞加莱球中。 由于潜在的双曲几何，这使我们可以通过同时捕获层次和相似性来学习符号数据的简约表示。 我们提出了一种有效的算法来学习基于黎曼优化的嵌入，并通过实验证明，Poincaré嵌入在表示能力和泛化能力方面可以显着优于具有潜在层次结构的数据的欧几里德插值。





对于有层级结构的网络来说，双曲插值比欧式差值更好。

- 插值的用途：
  - 补全图
  - 信息提取
- 对象：符号化的对象
  - similarity与distance
  - 如 单词、概念
  -  For instance, the existence of power-law distributions in datasets can often be traced back to hierarchical structures [29].  







## Poincare 插值



数据点在插值空间的距离代表它们语义的相似性。



我们假设：存在潜在的层级结构。除了similarity之外，我们还想证明，插值空间的层级结构可以有如下两个优点：

- 通过在嵌入空间中引入适当的结构偏差，我们旨在提高泛化性能以及运行时和存储器复杂性。
- 通过在嵌入空间中明确捕获层次结构，我们旨在获得关于符号之间的关系和各个符号的重要性的额外见解。









尽管我们假设存在层级结构，我们不假设可以直接得到这些结构。也就是说，揭示层级结构的过程将是完全<u>黑箱的、无监督的</u>。



### 庞加莱球模型



庞加莱球模型很适合进行基于梯度的优化。

令$\mathcal B^d = \{x\in \mathbb R^d,||x||\lt1\}$为$d$维开球，那么与庞加莱球模型相关的是黎曼流形$(\mathcal B^d,g_x).$ 也就是具有<u>黎曼度量</u> $g_x = (\frac{2}{1-||x||^2})^2g^E$ 的开的单位球（$g^E$代表欧式度量）。

两点距离定义为
$$
d(u,v)=arccosh(1+2\frac{||u-v||^2}{(1-||u||^2)(1-||v||^2)})
$$
边界：记为$\partial \mathcal B$ ，不属于圆盘（因为圆盘是开的）。

测地线：与$\partial \mathcal B$正交的曲线。

- 解释：由公式(1)，庞加莱圆盘上的距离变化是光滑的。这是找到连续层级变化的关键。

  - 例子：根结点放在中心，那么相对来讲，它跟其他结点的距离就会都比较小；叶结点会被放在靠近$\part \mathcal B$的位置，这个位置距离随着欧式距离的增长非常快，因为分母接近于$1.$ 
  - 公式(1)是对称的。所以层级结构完全由各结点到圆心的距离决定。
  - 由于自组织性，公式(1)可以支持一个无监督学习算法。
  - Equation (1) allows us therefore to learn embeddings that simultaneously capture the hierarchy of objects (through their norm) as well a their similarity (through their distance). 

  

单层级结构可以由2维庞加莱圆盘$(\mathcal B^2)$表示；本模型使用的是$(\mathcal B^d).$ 原因：

- 真实网络中，会有多重层级结构存在；
- 更大的插值维度可以减小插值模型优化的难度（更大自由度）

为了计算一个符号集$\mathcal S=\{x_i\}_{i=1}^n$的庞加莱插值$\Theta=\{\theta_i\}_{i=1}^n,\theta_i\in\mathcal B^d$，我们假设一个loss function：$\mathcal L(\Theta). $ 它鼓励语义相似在插值空间中位置相临近。

为了估计$\Theta,$ 我们求解下面的优化问题：
$$
\Theta'\leftarrow \arg\min_\Theta\mathcal L(\Theta),\\
s.t.\forall\theta_i\in\Theta:||\theta_i||\lt 1 .
$$

### 优化方法：随机黎曼优化（RSGD or RSVRG）

记：

- $\mathcal T_\theta\mathcal B$是点$\theta\in\mathcal B^d$的正交空间；
- $\nabla_R\in\mathcal T_\theta\mathcal B$为$\mathcal L(\theta)$的黎曼梯度，$\nabla_E$是它的欧式梯度。利用RSGD，参数由下式更新：$\theta_{t+1}=\mathscr R_{\theta_t}(-\eta_t\nabla_R\mathcal L(\theta_t))$
- 



















