import pandas as pd
import requests
import json
import time

def simulate_stream():
    url = "http://127.0.0.1:8000/predict"
    print("Loading test samples from creditcard.csv...")
    try:
        df = pd.read_csv('creditcard.csv')
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return
        
    # Pick a random mix of fraud and non-fraud items
    frauds = df[df['Class'] == 1].sample(5, random_state=42)
    normals = df[df['Class'] == 0].sample(5, random_state=42)
    
    test_samples = pd.concat([frauds, normals]).sample(frac=1, random_state=123).reset_index(drop=True)
    
    print("\nStarting simulated transaction stream...\n")
    for idx, row in test_samples.iterrows():
        payload = row.drop('Class').to_dict()
        true_label = int(row['Class'])
        
        start_t = time.time()
        try:
            response = requests.post(url, json=payload, timeout=2)
            if response.status_code == 200:
                result = response.json()
                api_latency = result.get('latency_ms', 0)
                network_latency = (time.time() - start_t) * 1000
                
                pred_label = 1 if result['is_fraud'] else 0
                match = "MATCH" if pred_label == true_label else "MISMATCH"
                
                print(f"Tx #{idx+1:02d} | True: {true_label} | Predicted: {pred_label} [{match}] | "
                      f"Prob: {result['fraud_probability']:.4f} | API: {api_latency:.2f}ms | Total RT: {network_latency:.2f}ms")
            else:
                print(f"Error for Tx #{idx+1}: {response.text}")
        except Exception as e:
            print(f"Connection failed: {e}. Ensure the FastAPI server is running on port 8000.")
            
        time.sleep(1)

if __name__ == '__main__':
    simulate_stream()
