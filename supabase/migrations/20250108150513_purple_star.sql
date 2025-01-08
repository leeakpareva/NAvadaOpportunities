/*
  # Initial NAVADA Database Schema

  1. New Tables
    - `profiles` - User profiles and preferences
    - `jobs` - Job listings with tech and artistic scores
    - `applications` - Track job applications
    - `documents` - Store document metadata
    - `job_tags` - Tags for job categorization

  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users
*/

-- Profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY REFERENCES auth.users ON DELETE CASCADE,
  email text UNIQUE NOT NULL,
  full_name text,
  avatar_url text,
  tech_preferences jsonb DEFAULT '[]'::jsonb,
  artistic_preferences jsonb DEFAULT '[]'::jsonb,
  location_preferences jsonb DEFAULT '[]'::jsonb,
  notification_settings jsonb DEFAULT '{"email": true, "in_app": true}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own profile"
  ON profiles FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id);

-- Jobs table
CREATE TABLE IF NOT EXISTS jobs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  company text NOT NULL,
  location text NOT NULL,
  description text NOT NULL,
  tech_score float NOT NULL DEFAULT 0,
  artistic_score float NOT NULL DEFAULT 0,
  url text,
  salary_range jsonb,
  requirements jsonb DEFAULT '[]'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Jobs are readable by all authenticated users"
  ON jobs FOR SELECT
  TO authenticated
  USING (true);

-- Job tags
CREATE TABLE IF NOT EXISTS job_tags (
  job_id uuid REFERENCES jobs ON DELETE CASCADE,
  tag text NOT NULL,
  PRIMARY KEY (job_id, tag)
);

ALTER TABLE job_tags ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Job tags are readable by all authenticated users"
  ON job_tags FOR SELECT
  TO authenticated
  USING (true);

-- Applications table
CREATE TABLE IF NOT EXISTS applications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES profiles ON DELETE CASCADE,
  job_id uuid REFERENCES jobs ON DELETE CASCADE,
  status text NOT NULL DEFAULT 'applied',
  notes text,
  applied_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(user_id, job_id)
);

ALTER TABLE applications ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can CRUD own applications"
  ON applications FOR ALL
  TO authenticated
  USING (auth.uid() = user_id);

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES profiles ON DELETE CASCADE,
  name text NOT NULL,
  type text NOT NULL,
  size integer NOT NULL,
  storage_path text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can CRUD own documents"
  ON documents FOR ALL
  TO authenticated
  USING (auth.uid() = user_id);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_jobs_updated_at
  BEFORE UPDATE ON jobs
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_applications_updated_at
  BEFORE UPDATE ON applications
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_documents_updated_at
  BEFORE UPDATE ON documents
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();