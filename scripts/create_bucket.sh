#!/bin/sh
/usr/bin/mc config host add myminio ${BUCKET_ENDPOINT} ${MINIO_ACCESS_KEY} ${MINIO_SECRET_KEY};
# /usr/bin/mc rm -r --force myminio/${MINIO_BUCKET};
# /usr/bin/mc rm -r --force myminio/${AWS_BUCKET_PRIVATE};
/usr/bin/mc mb -p myminio/${MINIO_BUCKET};
/usr/bin/mc policy set download myminio/${MINIO_BUCKET};
/usr/bin/mc policy set upload myminio/${MINIO_BUCKET};
exit 0;