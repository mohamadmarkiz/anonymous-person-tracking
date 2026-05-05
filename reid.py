import torch
import torchvision.transforms as transforms
import cv2
from PIL import Image
import torchreid


class ReID:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        
        self.model = torchreid.models.build_model(
            name='osnet_x0_25',
            num_classes=1000,
            pretrained=True
        )

        self.model.to(self.device)
        self.model.eval()

        
        self.transform = transforms.Compose([
            transforms.Resize((256, 128)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def extract(self, frame, bbox):
        x, y, w, h = bbox

        
        person = frame[y:y+h, x:x+w]

        if person.size == 0:
            return None

        
        person = cv2.cvtColor(person, cv2.COLOR_BGR2RGB)

        
        person = Image.fromarray(person)

        
        img = self.transform(person).unsqueeze(0).to(self.device)

        
        with torch.no_grad():
            feature = self.model(img)

        return feature.cpu().numpy().flatten()