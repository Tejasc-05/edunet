from django.core.management.base import BaseCommand
from waste.models import WasteCategory

class Command(BaseCommand):
    help = 'Populate waste categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'biodegradable',
                'icon': 'fa-leaf',
                'description': 'Natural waste that can be broken down by microorganisms. Includes food scraps, leaves, and paper products.',
                'color': '#2ecc71',
                'treatment_method': 'Composting and anaerobic digestion. Biodegradable waste is processed in composting facilities where microorganisms break it down into nutrient-rich soil.',
                'environmental_impact': 'When properly managed, biodegradable waste reduces methane emissions and creates valuable compost. However, if sent to landfills, it releases harmful greenhouse gases.',
            },
            {
                'name': 'plastic',
                'icon': 'fa-wine-bottle',
                'description': 'Non-biodegradable synthetic materials. Includes plastic bags, bottles, containers, and packaging materials.',
                'color': '#3498db',
                'treatment_method': 'Mechanical and chemical recycling. Plastics are sorted, cleaned, shredded, and melted to create new products or fuel.',
                'environmental_impact': 'Plastic waste persists in the environment for hundreds of years, causing harm to marine life and ecosystems. Recycling reduces landfill burden and conserves fossil fuels.',
            },
            {
                'name': 'ewaste',
                'icon': 'fa-laptop',
                'description': 'Electronic waste from discarded electrical and electronic equipment. Includes phones, computers, TVs, and appliances.',
                'color': '#9b59b6',
                'treatment_method': 'E-waste recycling facilities extract valuable metals and minerals through disassembly, shredding, and separation processes.',
                'environmental_impact': 'E-waste contains toxic materials like lead and mercury. Improper handling contaminates soil and water. Recycling recovers valuable resources and prevents environmental contamination.',
            },
            {
                'name': 'metal',
                'icon': 'fa-cog',
                'description': 'Metallic waste including aluminum, copper, iron, and steel from various sources.',
                'color': '#95a5a6',
                'treatment_method': 'Magnetic separation and smelting. Metal waste is sorted by type, shredded, and melted to create new products.',
                'environmental_impact': 'Metal recycling saves energy compared to primary production. Reduces mining impact and preserves natural resources.',
            },
            {
                'name': 'glass',
                'icon': 'fa-glass-martini-alt',
                'description': 'Glass waste from bottles, jars, windows, and other glass products.',
                'color': '#1abc9c',
                'treatment_method': 'Glass sorting, cleaning, and crushing. Processed glass is melted and reformed into new containers or used in construction.',
                'environmental_impact': 'Glass is infinitely recyclable without quality loss. Recycling glass saves energy and reduces need for virgin materials.',
            },
            {
                'name': 'hazardous',
                'icon': 'fa-skull-crossbones',
                'description': 'Dangerous waste including chemicals, batteries, medical waste, and pesticides that pose health and environmental risks.',
                'color': '#e74c3c',
                'treatment_method': 'Special treatment including chemical stabilization, incineration, and secure landfill disposal. Requires certified facilities.',
                'environmental_impact': 'Hazardous waste requires careful handling to prevent environmental and health hazards. Proper disposal prevents water contamination and health risks.',
            },
        ]

        for category_data in categories:
            category, created = WasteCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'icon': category_data['icon'],
                    'description': category_data['description'],
                    'color': category_data['color'],
                    'treatment_method': category_data['treatment_method'],
                    'environmental_impact': category_data['environmental_impact'],
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created category "{category.get_name_display()}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category "{category.get_name_display()}" already exists')
                )
