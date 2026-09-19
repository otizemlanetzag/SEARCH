import glob
from .db import connect, add_document
from .wet import iter_wet_records

def main():
    db=connect()
    count=0
    for filename in glob.glob("wet-data/*.wet"):
        with open(filename,"rb") as f:
            for url,title,text in iter_wet_records(f.read()):
                if len(text)<40:
                    continue
                add_document(db,url,title,text)
                count+=1
        print(f"indexed {filename}")
    db.commit()
    db.close()
    print(f"indexed documents: {count}")

if __name__=="__main__":
    main()
