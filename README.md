# MergeWizardPDF
<img width="779" alt="Screenshot 2023-10-03 at 22 08 38" src="https://github.com/Waleed2207/MergeWizardPDF/assets/62006481/8c4dc163-7344-4352-a3e9-60bc295e3df8">
<br>
<br>
<p>This architecture allows users to upload files, arrange them, and initiate a merge process. The files are processed and merged using an AWS Lambda function triggered by S3 events. The merged file is stored in another S3 bucket, and pre-signed URLs are generated to enable secure file downloads. The system is controlled by IAM permissions, and CloudWatch is used for logging and monitoring purposes.</p>
