#!/usr/bin/env python3
"""
CHAZON Medical Imaging SCADA - Database Migration Script
Migrates JSON files to SQLite databases to reduce file count and size
"""

import sqlite3
import json
import os
import sys
import glob
from pathlib import Path
from datetime import datetime

class DatabaseMigration:
    def __init__(self, db_path='database/chazon.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.stats = {
            'tags_migrated': 0,
            'samples_migrated': 0,
            'standards_migrated': 0,
            'errors': []
        }

    def connect(self):
        """Connect to SQLite database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"✓ Connected to database: {self.db_path}")

    def init_schema(self):
        """Initialize database schema"""
        schema_path = 'database/schema.sql'
        if not os.path.exists(schema_path):
            print(f"✗ Schema file not found: {schema_path}")
            return False

        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        try:
            self.cursor.executescript(schema_sql)
            self.conn.commit()
            print("✓ Database schema initialized")
            return True
        except Exception as e:
            print(f"✗ Error initializing schema: {e}")
            self.stats['errors'].append(('schema', str(e)))
            return False

    def migrate_tags(self):
        """Migrate all index/tag.json files to tags database"""
        print("\n📂 Migrating tag files...")

        tag_files = glob.glob('**/index/tag.json', recursive=True)
        print(f"   Found {len(tag_files)} tag files")

        for tag_file in tag_files:
            try:
                with open(tag_file, 'r') as f:
                    tag_data = json.load(f)

                # Insert main tag record
                self.cursor.execute('''
                    INSERT OR REPLACE INTO tags (
                        uuid, directory_path, directory_name, title, description,
                        icon, color_scheme, isa_level, parent_path,
                        has_plc, has_hmi, has_scada,
                        plc_path, hmi_path, scada_path,
                        readme_path, controls_path, status_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tag_data.get('UUID'),
                    tag_data.get('Directory_Path'),
                    tag_data.get('Directory_Name'),
                    tag_data.get('Title'),
                    tag_data.get('Description'),
                    tag_data.get('Icon'),
                    tag_data.get('Color_Scheme'),
                    tag_data.get('ISA_Level'),
                    tag_data.get('Parent_Path'),
                    tag_data.get('has_plc', False),
                    tag_data.get('has_hmi', False),
                    tag_data.get('has_scada', False),
                    tag_data.get('plc_path'),
                    tag_data.get('hmi_path'),
                    tag_data.get('scada_path'),
                    tag_data.get('README_Path'),
                    tag_data.get('Controls_Path'),
                    tag_data.get('Status_Path')
                ))

                tag_id = self.cursor.lastrowid

                # Insert features
                for idx, feature in enumerate(tag_data.get('Features', [])):
                    self.cursor.execute('''
                        INSERT INTO tag_features (tag_id, title, description, icon, sort_order)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (tag_id, feature.get('title'), feature.get('description'),
                          feature.get('icon'), idx))

                # Insert child directories
                for idx, child in enumerate(tag_data.get('Child_Directories', [])):
                    self.cursor.execute('''
                        INSERT INTO tag_child_directories
                        (tag_id, path, title, description, icon, page_count, sort_order)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (tag_id, child.get('path'), child.get('title'),
                          child.get('description'), child.get('icon'),
                          child.get('page_count', 0), idx))

                # Insert sibling directories
                for idx, sibling in enumerate(tag_data.get('Sibling_Directories', [])):
                    self.cursor.execute('''
                        INSERT INTO tag_sibling_directories
                        (tag_id, path, title, description, icon, sort_order)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (tag_id, sibling.get('path'), sibling.get('title'),
                          sibling.get('description'), sibling.get('icon'), idx))

                # Insert page links
                for idx, page in enumerate(tag_data.get('Page_Links', [])):
                    self.cursor.execute('''
                        INSERT INTO tag_page_links
                        (tag_id, path, name, icon, size, sort_order)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (tag_id, page.get('path'), page.get('name'),
                          page.get('icon'), page.get('size', 0), idx))

                # Insert quick actions
                for idx, action in enumerate(tag_data.get('Quick_Actions', [])):
                    self.cursor.execute('''
                        INSERT INTO tag_quick_actions
                        (tag_id, label, path, type, sort_order)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (tag_id, action.get('label'), action.get('path'),
                          action.get('type', 'primary'), idx))

                # Insert related files
                for idx, file in enumerate(tag_data.get('Related_Files', [])):
                    self.cursor.execute('''
                        INSERT INTO tag_related_files
                        (tag_id, path, name, type, sort_order)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (tag_id, file.get('path'), file.get('name'),
                          file.get('type'), idx))

                # Insert breadcrumb trail
                for idx, crumb in enumerate(tag_data.get('Breadcrumb_Trail', [])):
                    self.cursor.execute('''
                        INSERT INTO tag_breadcrumb_trail
                        (tag_id, path, title, icon, sort_order)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (tag_id, crumb.get('path'), crumb.get('title'),
                          crumb.get('icon'), idx))

                self.stats['tags_migrated'] += 1
                print(f"   ✓ {tag_file}")

            except Exception as e:
                print(f"   ✗ Error migrating {tag_file}: {e}")
                self.stats['errors'].append((tag_file, str(e)))

        self.conn.commit()
        print(f"\n   Total tags migrated: {self.stats['tags_migrated']}")

    def migrate_samples(self):
        """Migrate sample metadata to samples database"""
        print("\n📷 Migrating sample metadata...")

        # Define sample images we know about
        samples = [
            {
                'sample_id': 'xray_chest_001',
                'modality': 'XRay',
                'file_path': '/examples/xray/chest_sample.jpg',
                'file_name': 'chest_sample.jpg',
                'description': 'Chest X-ray - Normal',
                'body_part': 'Chest',
                'dataset_name': 'Sample'
            },
            {
                'sample_id': 'ct_lung_001',
                'modality': 'CT',
                'file_path': '/examples/ct/lung_sample.dcm',
                'file_name': 'lung_sample.dcm',
                'description': 'Lung CT - Nodule present',
                'body_part': 'Lung',
                'dataset_name': 'Sample'
            },
            {
                'sample_id': 'mri_brain_001',
                'modality': 'MRI',
                'file_path': '/examples/mri/brain_sample.nii.gz',
                'file_name': 'brain_sample.nii.gz',
                'description': 'Brain MRI - T1 weighted',
                'body_part': 'Brain',
                'study_type': 'T1',
                'dataset_name': 'Sample'
            }
        ]

        for sample in samples:
            try:
                self.cursor.execute('''
                    INSERT OR REPLACE INTO samples (
                        sample_id, modality, file_path, file_name, description,
                        body_part, study_type, dataset_name
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sample.get('sample_id'),
                    sample.get('modality'),
                    sample.get('file_path'),
                    sample.get('file_name'),
                    sample.get('description'),
                    sample.get('body_part'),
                    sample.get('study_type'),
                    sample.get('dataset_name')
                ))
                self.stats['samples_migrated'] += 1
                print(f"   ✓ {sample['sample_id']}")
            except Exception as e:
                print(f"   ✗ Error migrating sample {sample['sample_id']}: {e}")
                self.stats['errors'].append((sample['sample_id'], str(e)))

        self.conn.commit()
        print(f"\n   Total samples migrated: {self.stats['samples_migrated']}")

    def migrate_standards(self):
        """Migrate standards definitions to standards database"""
        print("\n⚙️  Migrating standards...")

        # Standards already seeded in schema.sql
        # Add PackML states
        try:
            standard_id = self.cursor.execute(
                "SELECT id FROM standards WHERE standard_name = 'PackML'"
            ).fetchone()[0]

            packml_states = [
                ('Idle', 2, 'Machine ready to start'),
                ('Starting', 3, 'Machine starting up'),
                ('Execute', 6, 'Machine running production'),
                ('Completing', 5, 'Completing current cycle'),
                ('Complete', 4, 'Cycle complete'),
                ('Stopping', 7, 'Controlled stop'),
                ('Stopped', 1, 'Machine stopped'),
                ('Aborting', 9, 'Emergency abort'),
                ('Aborted', 8, 'Machine aborted'),
                ('Clearing', 10, 'Clearing faults'),
                ('Resetting', 100, 'Resetting to idle'),
                ('Holding', 11, 'Process hold'),
                ('Held', 12, 'Process held'),
                ('Unholding', 13, 'Resuming from hold'),
                ('Suspending', 14, 'Suspending operation'),
                ('Suspended', 15, 'Operation suspended'),
                ('Unsuspending', 16, 'Resuming from suspend')
            ]

            for idx, (state_name, state_value, description) in enumerate(packml_states):
                self.cursor.execute('''
                    INSERT OR IGNORE INTO standard_states
                    (standard_id, state_name, state_value, description, sort_order)
                    VALUES (?, ?, ?, ?, ?)
                ''', (standard_id, state_name, state_value, description, idx))

            self.stats['standards_migrated'] += 1
            print("   ✓ PackML states")

        except Exception as e:
            print(f"   ✗ Error migrating PackML: {e}")
            self.stats['errors'].append(('PackML', str(e)))

        self.conn.commit()
        print(f"\n   Total standards migrated: {self.stats['standards_migrated']}")

    def migrate_models(self):
        """Migrate AI/ML model definitions"""
        print("\n🤖 Migrating AI/ML models...")

        models = [
            {
                'model_name': 'unet',
                'model_type': 'segmentation',
                'description': 'U-Net for organ segmentation',
                'precision': 'float32',
                'supported_organs': json.dumps(['liver', 'kidney', 'lungs', 'heart', 'brain'])
            },
            {
                'model_name': 'maskrcnn',
                'model_type': 'segmentation',
                'description': 'Mask R-CNN for instance segmentation',
                'precision': 'float32',
                'supported_organs': json.dumps(['tumor', 'lesion'])
            },
            {
                'model_name': 'yolov8',
                'model_type': 'detection',
                'description': 'YOLOv8 real-time detection',
                'precision': 'float32',
                'supported_targets': json.dumps(['nodule', 'lesion', 'tumor', 'fracture'])
            },
            {
                'model_name': 'biomedclip',
                'model_type': 'classification',
                'description': 'BiomedCLIP 768-dim embeddings',
                'precision': 'float32',
                'output_shape': json.dumps([768])
            }
        ]

        for model in models:
            try:
                self.cursor.execute('''
                    INSERT OR REPLACE INTO models (
                        model_name, model_type, description, precision,
                        supported_organs, supported_targets, output_shape
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    model.get('model_name'),
                    model.get('model_type'),
                    model.get('description'),
                    model.get('precision'),
                    model.get('supported_organs'),
                    model.get('supported_targets'),
                    model.get('output_shape')
                ))
                print(f"   ✓ {model['model_name']}")
            except Exception as e:
                print(f"   ✗ Error migrating model {model['model_name']}: {e}")

        self.conn.commit()

    def optimize_database(self):
        """Optimize database for performance"""
        print("\n🔧 Optimizing database...")

        try:
            self.cursor.execute('ANALYZE')
            self.cursor.execute('VACUUM')
            self.conn.commit()
            print("   ✓ Database optimized")
        except Exception as e:
            print(f"   ✗ Error optimizing: {e}")

    def print_statistics(self):
        """Print migration statistics"""
        print("\n" + "="*60)
        print("MIGRATION SUMMARY")
        print("="*60)

        # Get database file size
        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        db_size_mb = db_size / (1024 * 1024)

        print(f"\n📊 Statistics:")
        print(f"   Tags migrated:      {self.stats['tags_migrated']}")
        print(f"   Samples migrated:   {self.stats['samples_migrated']}")
        print(f"   Standards migrated: {self.stats['standards_migrated']}")
        print(f"   Database size:      {db_size_mb:.2f} MB")

        # Get record counts
        counts = {
            'Tags': self.cursor.execute('SELECT COUNT(*) FROM tags').fetchone()[0],
            'Features': self.cursor.execute('SELECT COUNT(*) FROM tag_features').fetchone()[0],
            'Child Directories': self.cursor.execute('SELECT COUNT(*) FROM tag_child_directories').fetchone()[0],
            'Samples': self.cursor.execute('SELECT COUNT(*) FROM samples').fetchone()[0],
            'Standards': self.cursor.execute('SELECT COUNT(*) FROM standards').fetchone()[0],
            'Models': self.cursor.execute('SELECT COUNT(*) FROM models').fetchone()[0]
        }

        print(f"\n📈 Database Records:")
        for name, count in counts.items():
            print(f"   {name:20} {count}")

        if self.stats['errors']:
            print(f"\n⚠️  Errors: {len(self.stats['errors'])}")
            for source, error in self.stats['errors'][:5]:  # Show first 5
                print(f"   {source}: {error}")

        print("\n✓ Migration complete!")
        print(f"   Database: {self.db_path}")
        print("="*60)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\n✓ Database connection closed")

    def run(self):
        """Run complete migration"""
        print("╔" + "="*58 + "╗")
        print("║" + " CHAZON Medical Imaging - Database Migration ".center(58) + "║")
        print("╚" + "="*58 + "╝")

        try:
            self.connect()
            if not self.init_schema():
                return False

            self.migrate_tags()
            self.migrate_samples()
            self.migrate_standards()
            self.migrate_models()
            self.optimize_database()
            self.print_statistics()

            return True

        except Exception as e:
            print(f"\n✗ Fatal error: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            self.close()


if __name__ == '__main__':
    migration = DatabaseMigration()
    success = migration.run()
    sys.exit(0 if success else 1)
