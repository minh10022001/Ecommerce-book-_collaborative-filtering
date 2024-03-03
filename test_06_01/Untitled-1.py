import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error
model = load_model('NFC_model.h5')
df_test =  pd.read_csv('ratings_v2_test.csv')

y = model.predict([df_test['id_customer'], df_test['id_book']])
mse = mean_squared_error(y, df_test['rating'])
print(mse)