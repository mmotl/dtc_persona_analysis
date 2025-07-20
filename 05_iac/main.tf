variable "project_id" {
  type        = string
  description = "The GCP project ID to deploy resources into."
}

variable "bucket_name" {
  type        = string
  description = "The desired name for the Google Cloud Storage bucket."
}

variable "bucket_admin_email" {
  type        = string
  description = "The email address of the user to be granted Storage Admin rights."
}

# Configure the Google Cloud provider
provider "google" {
  project = var.project_id
  region  = "europe-west3"
}

# Create a Google Cloud Storage bucket
resource "google_storage_bucket" "my_bucket" {
  name          = var.bucket_name 
  location      = "EU"
  storage_class = "STANDARD"

  # Optional: Enable versioning to keep a history of your objects
  versioning {
    enabled = true
  }

  # Optional: Set a lifecycle rule to delete old objects
  lifecycle_rule {
    condition {
      age = 30 # days
    }
    action {
      type = "Delete"
    }
  }
}

# Grant a specific principal the "Storage Admin" role on the bucket
resource "google_storage_bucket_iam_member" "storage_admin_member" {
  bucket = google_storage_bucket.my_bucket.name
  role   = "roles/storage.admin"
  member = "user:${var.bucket_admin_email}" 
}