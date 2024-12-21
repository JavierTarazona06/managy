import Image from "next/image";

const AmenityPanel = ({ amenity, onDeleteClick }) => {
    return (
        <button
            className="relative border-4 border-black rounded m-4 shadow-xl bg-white p-8 w-5/6 max-w-4xl h-96 mx-auto flex justify-between"
            onClick={() => onDeleteClick(amenity)}
        >
            <div className="flex-1 p-4">
                <h3 className="text-xl font-semibold">{amenity.name}</h3>
                <p className="mt-2">{amenity.description}</p>
                <p className="mt-2">Capacity: {amenity.capacity}</p>
            </div>
            <div className="flex-1 flex items-center justify-center">
                {amenity.image && (
                    <Image
                        src={amenity.image}
                        alt={`${amenity.name} image`}
                        width={300}
                        className="rounded-xl"
                        height={200}
                        layout="responsive"
                    />
                )}
            </div>
        </button>
    );
};
export default AmenityPanel;
