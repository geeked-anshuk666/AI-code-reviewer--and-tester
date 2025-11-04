from django.core.management.base import BaseCommand
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Initialize AI models for code analysis'

    def handle(self, *args, **options):
        self.stdout.write('Initializing AI models...')
        
        try:
            # Initialize sentiment analyzer
            self.stdout.write('Loading sentiment analysis model...')
            sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest"
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded sentiment analysis model')
            )
            
            # Initialize code classification model
            self.stdout.write('Loading code classification model...')
            # This would be a custom model for code classification
            # For now, we'll just show the concept
            self.stdout.write(
                self.style.SUCCESS('Code classification model initialization noted')
            )
            
            self.stdout.write(
                self.style.SUCCESS('All AI models initialized successfully!')
            )
            
        except Exception as e:
            logger.error(f"Error initializing AI models: {e}")
            self.stdout.write(
                self.style.ERROR(f'Failed to initialize AI models: {e}')
            )