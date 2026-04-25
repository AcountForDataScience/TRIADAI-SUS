# region save scores as dataframe
Save_Dataframe = False
if Save_Dataframe:  
  flattened_rows = []
  for run_key, data in score_table.items():

      print(f"raw data: \n {data} \n------------------")
      # 1. Extract metadata by index
      user_id   = data[0]
      user_name = data[1]
      run_id    = data[2]
      dirname   = data[3]
      datestamp = data[4]

      # 2. Iterate through the remaining items (the scores)
      # data[5:] takes everything from the 6th element to the end
      for score_tuple in data[5:]:
        print(score_tuple)
        value, test_name, *context = score_tuple

        flattened_rows.append({
            "user_id": user_id,
            "user_name": user_name,
            "date": datestamp,
            "run_id": run_id,
            "direction": dirname,
            "test_name": test_name,
            "score": value,
            "context": context
        })

  # 3. Create the DataFrame
  df = pd.DataFrame(flattened_rows)

  if os.getenv("COLAB_RELEASE_TAG"):
      from google.colab import drive
      #if not on Render, importing drive lib for files
      drive.mount('/content/drive/')
      save_path = '/content/drive/MyDrive/Colab/Telegram test/'
  elif os.getenv("RENDER"):
      save_path = '' #saving into current working directory
      # unless we want to invest into
  else:
      save_path = os.path.join(os.getcwd(), 'temp')
      # saves into CWD / temp subpath

  scorefile = save_path + 'scores.csv'
  print(scorefile)
  if os.path.isfile(scorefile):
      print("Appending scores")
      # mode = 'a' for append
      df.to_csv(scorefile, mode='a', index=False, header=False)
  else:
      print("File not found, creating new...")
      df.to_csv(scorefile, encoding='utf-8', index=False)

Test_Score_Dataframe = False

import pandas as pd

if Test_Score_Dataframe:
  flattened_rows = []
  for run_key, data in score_table.items():

      print(f"raw data: \n {data} \n------------------")
      # 1. Extract metadata by index
      user_id   = data[0]
      user_name = data[1]
      run_id    = data[2]
      dirname   = data[3]
      datestamp = data[4]

      # 2. Iterate through the remaining items (the scores)
      # data[5:] takes everything from the 6th element to the end
      for score_tuple in data[5:]:
        print(score_tuple)
        value, test_name, *context = score_tuple

        flattened_rows.append({
            "user_id": user_id,
            "user_name": user_name,
            "date": datestamp,
            "run_id": run_id,
            "direction": dirname,
            "test_name": test_name,
            "score": value,
            "context": context
        })

  # 3. Create the DataFrame
  df = pd.DataFrame(flattened_rows)


  print(f"  > DataFrame for the score table: <\n{df}")

  # 4. Score sum
  summary_df = df.groupby(['user_id', 'run_id', 'direction']).agg(
        total_score=('score', 'sum'),
        test_count=('test_name', 'count')
    ).reset_index()

  print(f"---< Score summary: >--- \n{summary_df}\n------------------------")

# endregion

print("Dataframe tested")