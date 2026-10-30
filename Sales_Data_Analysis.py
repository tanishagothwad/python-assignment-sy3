
import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv("sales.csv")

# Display data
print(df)

# Calculate total and average sales
print("Total Sales:", df["Sales"].sum())
print("Average Sales:", df["Sales"].mean())

# Find month with highest sales
print("Month with Highest Sales:")
print(df.loc[df["Sales"].idxmax()])

# Group sales by product category
category_sales = df.groupby("Category")["Sales"].sum()
print("Sales by Product Category:")
print(category_sales)

# Bar chart: Sales by category
category_sales.plot(kind="bar")
plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.show()

# Line chart: Monthly sales trends
plt.plot(df["Month"], df["Sales"], marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()

# Pie chart: Percentage contribution of each category
category_sales.plot(kind="pie", autopct="%1.1f%%")
plt.title("Sales Contribution by Category")
plt.ylabel("")
plt.show()
