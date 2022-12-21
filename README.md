# HSR-Optimization
A linear program implemented with Gurobi to solve for the optimal city pairs for high speed rail in the United States.

## Prerequisites

- Python
- Jupyter notebooks
- the Gurobi Python package

## Instructions

To run the analysis, first run the cells of the `combinedStat.ipynb` notebook in order. Then run the `optimize.py` file.

## `combinedStat.ipynb`

### Parameters: 
- `minDist` is the number of miles in our travel demand calculation where travel demand no longer improves as $d < $`minDist`
	 - This shows up in our model as $T_{i, j}=\left(\frac{P_i^{0.8} \times P_j^{0.8}}{\max \left(d_{i, j},  {\tt minDist}\right)^2}\right)$

## `optimize.py`

### Parameters: 
- `trackAmt` is the "budget" you have for building track
- `penaltyAmt` is the amount you assign as a penalty in track miles to decrease your track "budget" for each new route you add 
- `perCity` is the maximum number of train routes that any given city can have