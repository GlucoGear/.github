import os
import sys

def main(aws_profile, root_path):
    rootDir = os.path.expanduser('~')
    print(root_path)

    try:
        os.mkdir(f"{root_path}.aws")
    except OSError:
        print (f"Creation of the directory {root_path}.aws failed")
    else:
        print (f"Successfully created the directory {root_path}.aws")

    ORG_TF_AWS_KEY_ID = os.environ["ORG_TF_AWS_KEY_ID"]
    ORG_TF_AWS_SECRET_KEY = os.environ["ORG_TF_AWS_SECRET_KEY"]
    
    HML_TF_AWS_KEY_ID = os.environ["HML_TF_AWS_KEY_ID"]
    HML_TF_AWS_SECRET_KEY = os.environ["HML_TF_AWS_SECRET_KEY"]
    
    PRD_TF_AWS_KEY_ID = os.environ["PRD_TF_AWS_KEY_ID"]
    PRD_TF_AWS_SECRET_KEY = os.environ["PRD_TF_AWS_SECRET_KEY"]    

    # DL_TF_AWS_KEY_ID = os.environ["DL_TF_AWS_KEY_ID"]
    # DL_TF_AWS_SECRET_KEY = os.environ["DL_TF_AWS_SECRET_KEY"]    

    fileAws = open(f"{root_path}.aws/credentials","w")

    fileAws.write("[org]\n")
    fileAws.write(f"aws_access_key_id={ ORG_TF_AWS_KEY_ID }\n")
    fileAws.write(f"aws_secret_access_key={ ORG_TF_AWS_SECRET_KEY }\n\n")

    fileAws.write("[dev]\n")
    fileAws.write(f"aws_access_key_id={ HML_TF_AWS_KEY_ID }\n")
    fileAws.write(f"aws_secret_access_key={ HML_TF_AWS_SECRET_KEY }\n\n")

    fileAws.write("[hml]\n")
    fileAws.write(f"aws_access_key_id={ HML_TF_AWS_KEY_ID }\n")
    fileAws.write(f"aws_secret_access_key={ HML_TF_AWS_SECRET_KEY }\n\n")

    fileAws.write("[prd]\n")
    fileAws.write(f"aws_access_key_id={ PRD_TF_AWS_KEY_ID }\n")
    fileAws.write(f"aws_secret_access_key={ PRD_TF_AWS_SECRET_KEY }\n\n")

    # fileAws.write("[dl]\n")
    # fileAws.write(f"aws_access_key_id={ DL_TF_AWS_KEY_ID }\n")
    # fileAws.write(f"aws_secret_access_key={ DL_TF_AWS_SECRET_KEY }\n")
    # fileAws.write(f"region=sa-east-1")


    fileAws.close()    

    os.environ["AWS_PROFILE"] = aws_profile.lower()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])