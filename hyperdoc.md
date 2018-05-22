[TOC]

## 映射方法

为了找到双曲因特网映射，我们使用了$\mathbb H^2$和$\mathbb S^1$的等价性。这种等价性建立了结点的期望度$\kappa$和半径$r$之间的联系。角度参数$\theta$在两个模型中是相同的。因此，给定一个结点$i$，我们的**目标**是找到它的期望度和角参数$\{\kappa_i,\theta_i\}.$，来最好地适应$\mathbb S^1$模型，然后再映射到$\mathbb H^2$
$$
h:\kappa\rightarrow r(\mathbb S^1\longrightarrow \mathbb H^2)
$$
多亏了这种同构性，两个模型可以生成统计同构的拓扑网络。但是，在$\mathbb H^2$上进行贪婪搜索的效率更高。因为双曲测地线与拓扑最短路径在无标度网络上是一致的。这种一致性的成因是，有效距离使用连接概率来表示的。2⃣而这种连接概率函数实际上是双曲函数。所以$\mathbb H^2$实际上就是将有效距离翻译到双曲空间。

综上所述，$\mathbb H^2$是路由选择更好的表示办法。尽管我们用$\mathbb S^1$来找Internet map。它的优点是对于$\kappa$和$\theta$的统计推断可以独立进行。

### $\mathbb S^1$模型生成网络

- 步骤：

  1. 将$N$个点按均匀分布放在半径为$\frac{N}{2\pi}$的圆周，使得点的密度函数为$\mathbb{1}$ ;

  2. 给每个点一个期望度$\kappa_i,i=1,2,3,\cdots$，为了使得生成的网络为scale-free的，我们需要$\rho(\kappa)=\kappa_0^{r-1}(\gamma-1)\kappa^{-\gamma},\kappa\geq\kappa_0=\bar{k}\frac{\gamma-2}{\gamma-1}$；$\kappa_0$为允许的最小度，$\bar{k}$为平均度；

  3. 根据期望度$\kappa_i$建立连接概率$p(\chi)$: 设圆周上两点$i,j$的角距离为$\Delta \theta$, 那么它们在圆周上相距$d:=\Delta\theta\frac{N}{2\pi}$。令他们的***有效距离***为
     $$
     \chi:=\frac{d}{\mu\kappa_i\kappa_j}=\frac{\Delta\theta N}{2\pi\mu\kappa_i\kappa_j} \\\ \mu:=f(\bar{k})
     $$
     从而定义***连接概率*** (Fermi-Dirac 分布，实际上可以取任何可积函数)
     $$
     p(\chi)  = p(\Delta\theta,\kappa_i,\kappa_j)=\frac{1}{1+\chi^\beta}=\frac{1}{1+(\frac{\Delta\theta N}{2\pi\mu\kappa_i\kappa_j})^\beta} \\\
     =\frac{{(2\pi\mu\kappa_i\kappa_j})^\beta}{({2\pi\mu\kappa_i\kappa_j})^\beta+(\Delta\theta N)^\beta} \\\
     \beta=\frac{1}{T},\text{是一个控制网络的集聚性的参数}
     $$
     在这个连接概率下，$\mu=\frac{\beta}{2\pi\bar k}\sin[\frac{\pi}{\beta}].$ 

  

  

### $\mathbb S^1$到$\mathbb H^2$的映射

- 步骤：

  1. 保持角参数$\theta$不变；

  2. 期望度映射为$\mathbb H^2$上的$r$：
     $$
     r=R-2\ln\frac{\kappa}{\kappa_0}\\\
     \text{其中,  }R=2\ln[\frac{N}{\pi\mu\kappa^2_0}]
     $$


## 似然估计



- 目标：给定路由网络（AS图），将其映射到$\mathbb S^1$上。

- 最大似然估计（MLE）：计算一个后验概率$\mathcal L(a_{ij}|\gamma,\beta,\bar k),$ 代表邻接矩阵$\{a_{ij}\}$由参数为$\gamma,\beta,\bar k$的$\mathbb S^1$模型生成的概率。
  $$
  \mathcal L(a_{ij}|\gamma,\beta,\bar k)=\int \cdots\int \mathcal L(a_{ij},\{\kappa_i,\theta_i\}|\gamma,\beta,\bar k)\prod_{i=1}^{N}d\theta_id\kappa_i 
  $$
   我们需要的是$\mathcal L(\{\kappa_i,\theta_i\}|a_{ij},\beta,\bar k). $根据Bayes公式和条件概率公式：
  $$
  \begin{align}
  
  &\mathcal L(\{\kappa_i,\theta_i\}|a_{ij},\gamma,\beta,\bar k)\\\
  = &\frac{\mathcal L(a_{ij},\{\kappa_i,\theta_i\}|\gamma,\beta,\bar k)}{\mathcal L(a_{ij}|\gamma,\beta,\bar k)},&\text{分子是(5)中的被积分函数，分母是(5)左面}\\\
  =&\frac{P(\{\kappa_i,\theta_i\})\mathcal L(a_{ij}|\{\kappa_i,\theta_i\},\gamma,\beta,\bar k)}{\mathcal L(a_{ij}|\gamma,\beta,\bar k)}, & \text{其中}P(\{\kappa_i,\theta_i\})=\frac{\prod_{i=1}^{N}\rho(\kappa_i)}{(2\pi)^N}
  
  \end{align}
  $$
  (8)分子的第二项是连接概率！也即$\prod_{i<j}p(\chi_{ij})^{a_{ij}}(1-p(\chi_{ij}))^{1-a_{ij}}.$ 

- 根据原始数据，我们可以得到平均度$\bar k$，幂律指数$\gamma$，以及聚集系数$\beta=\frac{1}{T}. $ 所以未知量只有$\kappa_i,\theta_i,i=1,2,3,\cdots$ 我们的目标就是找到最合适的$\kappa_i,\theta_i,$ 使得**对数似然函数**$$\ln \mathcal L(\{\kappa_i,\theta_i\}|a_{ij},\gamma,\beta,\bar k)$$最大：
  $$
  \ln \mathcal L(\{\kappa_i,\theta_i\}|a_{ij},\gamma,\beta,\bar k)=C-\gamma\sum_{i=1}^N \ln(\kappa_i)+\sum_{i<j}a_{ij}\ln p(\chi_{ij})-\sum_{i<j}(1-a_{ij})\ln (1-p(\chi_{ij}))
  $$


###对$\kappa$的估计

(9)式对$\kappa_i$进行微分，得到
$$
\frac{\partial}{\partial\kappa_i}\ln \mathcal L=-\frac{\gamma}{\kappa_i}-\frac{\beta}{\kappa_i}(\sum_{j\ne i}p(\chi_{ji})-\sum_j a_{ji})
$$
其中$\sum_{j\ne i}p(\chi_{ji})=\kappa_i,$ 也就是点$i$的期望度；$\sum_ja_{ji}$为网络中的实际度。用$k_i$代表点$i$的实际度，那么使得似然函数取得最大值的点，就是$\kappa_l^*=k_l-\frac{\gamma}{\beta}.$ 注意到它有可能小于最小度$\kappa_0,$ 我们取
$$
\begin{equation}
k_l^*=\max
\begin{cases}
k_l-\frac{\gamma}{\beta},\\\
\kappa_0=\frac{\gamma-2}{\gamma-1}\bar k
\end{cases}
\end{equation}
$$

###对$\theta$的估计

为使得(6)式最大，我们观察(8)式，只需让$\ln \mathcal L(a_{ij}|\{\kappa_i,\theta_i\},\gamma,\beta,\bar k)$最大即可。也就是
$$
\begin{align}
&\ln \mathcal L(a_{ij}|\{\kappa_i^*,\theta_i\},\gamma,\beta,\bar k)\\\
=&\sum_{i<j}\left(a_{ij}\ln p(\chi_{ij})+(1-a_{ij})\ln [1-p(\chi_{ij})] \right)\\\
=&\sum_{a_{ij}=1}\ln p(\chi_{ij})+\sum_{a_{ij=0}}\ln [1-p(\chi_{ij})]
\end{align}
$$
我们注意到，如果$i$与$j$之间有边，那么$a_{ij}=1$；反之为$0.$ 所以上面式子传达的信息就是，如果有连边，那么$p(\chi_{ij})$要很大，反之要很小。考虑到$\chi_{ij}=\frac{N\bar k \Delta\theta_{ij}}{\beta\sin(\frac{\pi}{\beta})\kappa_i\kappa_j},$ 所以要巧妙地设计一套$\theta$，使得总似然函数最大。

式子(14)对$\theta$ 的最小值没有分析解，所以我们必须考虑数值近似。这依赖于最大似然估计法与核估计。下面两种算法分别给出了

#### standard Metropolis-Hasting 算法（全局）



#### localized Metropolis-Hasting 算法（局部）



## 其他参数估计

需要对其他的三个参数进行估计：

- 平均度$\bar k$
- 度分布指数$\gamma$
- 临界概率中的指数$\beta$

### $\gamma$的估计



对结点的度分布进行powerlaw拟合。

文章中的结果是$\gamma=2.1$



### $N$和$\bar k$的估计



$N$也是需要顾及的。因为在$\mathbb S^1$模型中，会产生度为$0$的结点。平均度会被计算为$\bar k =\sum_{k=0}kP(k).$ 但是在真实网络拓扑中，没有结点的度为$0$，所以参数需要一个简单的修正：
$$
N=\frac{N_{obs}}{1-P(0)}
$$
第二个问题是**有限样本效应**。在$\gamma\approx2$时，有限样本效应十分明显。假设我们要生成一个样本量为$N$的网络，由于网络是有限的，结点的期望度会存在一个截断，$\kappa_c$ 。带截断的度分布的一阶矩为
$$
<\kappa(N)>=\bar k (1-[\frac{\kappa_0}{\kappa_c}]^{\gamma-2}):=\bar k \alpha(\kappa_0,\kappa_c)
$$
对热力学极限$\kappa_c\longrightarrow\infty$有$\alpha\longrightarrow 1$ . 但是如果$\gamma\rightarrow2$， 这个收敛速度就会非常慢。

