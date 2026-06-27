import seaborn as sns
import matplotlib.pyplot as plt

def set_skin():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams['figure.figsize'] = (10, 5)

def plot_counts(df, col, title=None):
    set_skin()
    order = df[col].value_counts().index
    ax = sns.countplot(data=df, x=col, order=order)
    if title: ax.set_title(title)
    return ax