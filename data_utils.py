from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler
import torchvision.transforms as transforms
from dataset import UrbanSoundDataset

def prepare_dataloader(dataset: Dataset, batch_size: int):
    return DataLoader(
        dataset,
        batch_size=batch_size,
        pin_memory=True,
        shuffle=False,
        sampler=DistributedSampler(dataset)
    )
    
def prepare_datasets(args):
    # Define the postprocessing transformations

    
    # Create the training dataset
    train_dataset = UrbanSoundDataset(
        args.data_folder_name,
    )

    # Create the validation dataset
    val_dataset = UrbanSoundDataset(
        args.data_folder_name,
    )
    
    return train_dataset, val_dataset