import os
import cv2  # Only OpenCV for basic image processing
import numpy as np
from .utils import download_image

class TrueFaceVerifier:
    def __init__(self, known_faces_dir="known_faces/"):
        self.known_faces_dir = known_faces_dir
        self.known_encodings = self._load_known_faces()

    def _load_known_faces(self):
        """Load and encode known faces from directory."""
        encodings = {}
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith(('.jpg', '.png')):
                img_path = os.path.join(self.known_faces_dir, filename)
                face_encoding = self._extract_face_encoding(img_path)
                if face_encoding is not None:
                    encodings[filename] = face_encoding
        return encodings

    def _extract_face_encoding(self, img_path):
        """Extract face features using basic image processing."""
        img = cv2.imread(img_path)
        if img is None:
            return None
        
        # Convert to grayscale and detect faces (simplest approach)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None
        
        # Return face region as a "fake encoding" (custom logic)
        (x, y, w, h) = faces[0]
        face_region = gray[y:y+h, x:x+w]
        return face_region.flatten()  # Simple flattening as a placeholder

    def verify_face(self, image_url):
        """Verify if the downloaded image matches any known face."""
        try:
            # Download image
            temp_img = download_image(image_url)
            if not temp_img:
                return {"error": "Image download failed"}
            
            # Extract encoding
            input_encoding = self._extract_face_encoding(temp_img)
            if input_encoding is None:
                return {"is_verified": False, "confidence": 0}
            
            # Compare with known faces (custom similarity metric)
            best_match = None
            best_score = 0
            
            for name, known_encoding in self.known_encodings.items():
                # Simple similarity score (cosine similarity)
                score = self._cosine_similarity(input_encoding, known_encoding)
                if score > best_score:
                    best_score = score
                    best_match = name
            
            # Threshold for verification (adjust as needed)
            is_verified = best_score > 0.6
            return {
                "is_verified": is_verified,
                "confidence": best_score,
                "matched_face": best_match if is_verified else None
            }
        except Exception as e:
            return {"error": str(e)}
        finally:
            if os.path.exists(temp_img):
                os.remove(temp_img)

    def _cosine_similarity(self, vec1, vec2):
        """Basic cosine similarity between two vectors."""
        dot = np.dot(vec1, vec2)
        norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        return dot / (norm + 1e-10)  # Avoid division by zero

# Singleton instance
verifier = TrueFaceVerifier()

def verify_face(image_url):
    return verifier.verify_face(image_url)