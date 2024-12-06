import csv
from .models import StaffMember
from fuzzywuzzy import process
from django.db.models import Q

def search_staff(query):
    """
    Enhanced staff search using fuzzy matching and substring fallback.
    """
    if not query:
        return None

    # Fetch all staff names and map to IDs
    staff_members = StaffMember.objects.values_list('id', 'name')
    staff_names = {staff[1]: staff[0] for staff in staff_members}

    # Fuzzy matching for names
    best_match = process.extractOne(query, staff_names.keys())

    if best_match and best_match[1] >= 70:  # Adjusted threshold for better recognition
        matched_id = staff_names[best_match[0]]
        return StaffMember.objects.get(id=matched_id)

    # Substring fallback search
    matches = StaffMember.objects.filter(Q(name__icontains=query) | Q(role__icontains=query))
    return matches.first() if matches.exists() else None

def update_staff_data_from_csv(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            staff, created = StaffMember.objects.update_or_create(
                name=row['Name'],
                defaults={
                    'role': row['Role'],
                    'email': row['Email'],
                    'phone': row['Phone'],
                    'address': row['Address'],
                    'tags': row['Tags'],
                    'profile_description': row['Profile Description'],
                    'news': row['News'],
                }
            )
