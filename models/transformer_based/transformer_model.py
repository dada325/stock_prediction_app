import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification

# Constants
MODEL_NAME = 'bert-base-uncased'
MODEL_PATH = 'models/transformer_model'
MAX_LEN = 250

# Load the tokenizer
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

def encode_sequences(sequences):
    """Tokenize and encode sequences."""
    return tokenizer(sequences, padding='max_length', truncation=True, max_length=MAX_LEN, return_tensors='tf')

def train_transformer_model(train_sequences, train_labels, epochs=4, batch_size=16):
    """Fine-tune the transformer model on our dataset."""
    
    # Load the base BERT model
    model = TFBertForSequenceClassification.from_pretrained(MODEL_NAME)
    
    # Prepare data
    train_encodings = encode_sequences(train_sequences)
    train_dataset = tf.data.Dataset.from_tensor_slices((
        {"input_ids": train_encodings['input_ids'], "attention_mask": train_encodings['attention_mask']},
        train_labels
    )).shuffle(1000).batch(batch_size)

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)
    model.compile(optimizer=optimizer, loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
    model.fit(train_dataset, epochs=epochs)

    # Save the fine-tuned model
    model.save_pretrained(MODEL_PATH)
    tokenizer.save_pretrained(MODEL_PATH)

def load_transformer_model():
    """Load the fine-tuned transformer model for inference."""
    model = TFBertForSequenceClassification.from_pretrained(MODEL_PATH)
    return model
