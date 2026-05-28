```
import sys  
import json  
import csv  
import os  
  
  
def json_to_csv(json_filename, csv_filename):  
    with open(json_filename, 'r', encoding='utf-8') as f:  
        data = json.load(f)  
  
    with open(csv_filename, 'w', encoding='utf-8', newline='') as f:  
        writer = csv.writer(f)  
  
        writer.writerow([  
            "movie_id", "movie_name", "movie_rating",  
            "movie_author1", "movie_author2",  
            "movie_type", "movie_language",  
            "movie_imdb", "movie_date", "movie_area"  
        ])  
  
        for item in data:  
            movie_id = item.get("movie_id", "")  
            movie_name = item.get("movie_name", "")  
            movie_rating = item.get("movie_rating", "")  
  
            authors = item.get("movie_author", [])  
            movie_author1 = authors[0] if len(authors) > 0 else ""  
            movie_author2 = authors[1] if len(authors) > 1 else ""  
  
            movie_type = item.get("movie_type", "")  
            movie_language = item.get("movie_language", "")  
            movie_imdb = item.get("movie_imdb", "")  
            movie_date = item.get("movie_date", "")  
            movie_area = item.get("movie_area", "")  
  
            writer.writerow([  
                movie_id, movie_name, movie_rating,  
                movie_author1, movie_author2,  
                movie_type, movie_language,  
                movie_imdb, movie_date, movie_area  
            ])  
  
  
def csv_to_json(csv_filename, json_filename):  
    if not os.path.exists(csv_filename):  
        return  
  
    json_data = []  
    with open(csv_filename, 'r', encoding='utf-8') as f:  
        reader = csv.reader(f)  
  
        header = next(reader, None)  
        if header is None:  
            return  
  
        for row in reader:  
            if not row:  
                continue  
  
            movie_id = row[0]  
            movie_name = row[1]  
  
            try:  
                movie_rating = float(row[2])  
            except ValueError:  
                movie_rating = row[2]  
  
            movie_author1 = row[3]  
            movie_author2 = row[4]  
  
            # 重新组装作者列表  
            movie_author = []  
            if movie_author1:  
                movie_author.append(movie_author1)  
            if movie_author2:  
                movie_author.append(movie_author2)  
  
            movie_type = row[5]  
            movie_language = row[6]  
            movie_imdb = row[7]  
            movie_date = row[8]  
            movie_area = row[9]  
  
            item = {  
                "movie_id": movie_id,  
                "movie_name": movie_name,  
                "movie_rating": movie_rating,  
                "movie_author": movie_author,  
                "movie_type": movie_type,  
                "movie_language": movie_language,  
                "movie_imdb": movie_imdb,  
                "movie_date": movie_date,  
                "movie_area": movie_area  
            }  
            json_data.append(item)  
  
    with open(json_filename, 'w', encoding='utf-8') as f:  
        json.dump(json_data, f, indent=4, ensure_ascii=False)  
  
  
def main():  
    if len(sys.argv) < 3:  
        return  
    flag = sys.argv[1]  
    input_file = sys.argv[2]  
    filename, _ = os.path.splitext(input_file)  
  
    if flag == '-p':  
        json_to_csv(input_file, f"{filename}.csv")  
    elif flag == '-b':  
        csv_to_json(input_file, f"{filename}.json")  
  
  
if __name__ == "__main__":  
    main()
```