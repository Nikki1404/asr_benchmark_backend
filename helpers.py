def calculate_statistics(data):
    """Helper function to calculate statistics from dashboard data"""
    if not data:
        return {}
    
    total_files = len(data)
    avg_wer = sum(row.get('WER Score', 0) for row in data) / total_files if total_files > 0 else 0
    avg_inference_time = sum(row.get('Inference time (in sec)', 0) for row in data) / total_files if total_files > 0 else 0
    
    return {
        'totalFiles': total_files,
        'avgWer': round(avg_wer, 4),
        'avgInferenceTime': round(avg_inference_time, 4)
    }

def calculate_model_performance(data):
    """Helper function to calculate per-model performance statistics"""
    if not data:
        return []
    
    models = {}
    for row in data:
        model = row.get('Model', 'Unknown')
        if model not in models:
            models[model] = {'wer_scores': [], 'inference_times': []}
        
        models[model]['wer_scores'].append(row.get('WER Score', 0))
        models[model]['inference_times'].append(row.get('Inference time (in sec)', 0))
    
    model_performance = []
    for model, stats in models.items():
        avg_wer = sum(stats['wer_scores']) / len(stats['wer_scores']) if stats['wer_scores'] else 0
        avg_inference = sum(stats['inference_times']) / len(stats['inference_times']) if stats['inference_times'] else 0
        
        model_performance.append({
            'model': model,
            'avgWer': round(avg_wer, 4),
            'avgInferenceTime': round(avg_inference, 4)
        })
    
    return model_performance