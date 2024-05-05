from sqlalchemy.orm import Session
from utils import seed_model
import sys
sys.path.append("..")
from argon2 import PasswordHasher


def seed_disciplines(db:Session):
    from db.main_model import DisciplineModel
    
    data = [
        {
            'id': 1, 'slug': 'computer-science-it', 'discipline_name': 'Computer Science & IT',
            'icons': """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M17.0722 1.66669H23.9279C26.5804 1.66666 28.7027 1.66664 30.3987 1.84542C32.1445 2.02944 33.6295 2.41777 34.9245 3.32445C35.8004 3.93779 36.5622 4.69965 37.1755 5.57557C38.0824 6.87047 38.4707 8.35549 38.6547 10.1013C38.8334 11.7973 38.8334 13.9197 38.8334 16.5721V16.7612C38.8334 19.4137 38.8334 21.536 38.6547 23.232C38.4707 24.9779 38.0824 26.4629 37.1755 27.7579C36.5622 28.6337 35.8004 29.3955 34.9245 30.0089C33.6295 30.9157 32.1445 31.304 30.3987 31.488C28.7027 31.6667 26.5804 31.6667 23.9279 31.6667H17.0721C14.4197 31.6667 12.2973 31.6667 10.6013 31.488C8.85549 31.304 7.37047 30.9157 6.07557 30.0089C5.19965 29.3955 4.43779 28.6337 3.82445 27.7579C2.91777 26.4629 2.52944 24.9779 2.34542 23.232C2.16664 21.536 2.16666 19.4137 2.16669 16.7612V16.5722C2.16666 13.9197 2.16664 11.7973 2.34542 10.1013C2.52944 8.35549 2.91777 6.87047 3.82445 5.57557C4.43779 4.69965 5.19965 3.93779 6.07557 3.32445C7.37047 2.41777 8.85549 2.02944 10.6013 1.84542C12.2973 1.66664 14.4197 1.66666 17.0722 1.66669ZM10.9507 5.16039C9.47956 5.31545 8.62969 5.6053 7.98749 6.05497C7.43009 6.44527 6.94527 6.93009 6.55497 7.48749C6.1053 8.12969 5.81545 8.97955 5.66039 10.4507C5.50219 11.9515 5.50002 13.898 5.50002 16.6667C5.50002 19.4354 5.50219 21.3819 5.66039 22.8827C5.81545 24.3539 6.1053 25.2037 6.55497 25.8459C6.94527 26.4034 7.43009 26.8882 7.98749 27.2784C8.62969 27.728 9.47956 28.0179 10.9507 28.173C12.4515 28.3312 14.398 28.3334 17.1667 28.3334H23.8334C26.602 28.3334 28.5485 28.3312 30.0494 28.173C31.5205 28.0179 32.3704 27.728 33.0125 27.2784C33.57 26.8882 34.0549 26.4034 34.445 25.8459C34.8947 25.2037 35.1845 24.3539 35.3397 22.8827C35.4979 21.3819 35.5 19.4354 35.5 16.6667C35.5 13.898 35.4979 11.9515 35.3397 10.4507C35.1845 8.97955 34.8947 8.12969 34.445 7.48749C34.0549 6.93009 33.57 6.44527 33.0125 6.05497C32.3704 5.6053 31.5205 5.31545 30.0494 5.16039C28.5485 5.00219 26.602 5.00002 23.8334 5.00002H17.1667C14.398 5.00002 12.4515 5.00219 10.9507 5.16039Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M25.9042 12.2453C25.3033 12.9425 25.3813 13.9949 26.0785 14.5958L28.1228 16.3578C28.2587 16.475 28.376 16.5761 28.4793 16.6667C28.376 16.7574 28.2587 16.8585 28.1228 16.9757L26.0785 18.7377C25.3813 19.3385 25.3033 20.391 25.9042 21.0882C26.5052 21.7854 27.5575 21.8635 28.2548 21.2625L30.299 19.5005C30.3195 19.4829 30.3402 19.465 30.3608 19.4474C30.7358 19.1244 31.1343 18.781 31.4257 18.4519C31.7552 18.0797 32.1667 17.489 32.1667 16.6667C32.1667 15.8444 31.7552 15.2537 31.4257 14.8815C31.1343 14.5524 30.7358 14.2092 30.3608 13.8861C30.3402 13.8683 30.3195 13.8506 30.299 13.8329L28.2548 12.0709C27.5575 11.47 26.5052 11.548 25.9042 12.2453Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M15.0957 12.2453C15.6967 12.9425 15.6187 13.9949 14.9214 14.5958L12.8772 16.3578C12.7413 16.475 12.6241 16.5761 12.5207 16.6667C12.6241 16.7574 12.7413 16.8585 12.8772 16.9757L14.9214 18.7377C15.6187 19.3385 15.6967 20.391 15.0957 21.0882C14.4948 21.7854 13.4424 21.8635 12.7452 21.2625L10.7009 19.5005C10.6804 19.4829 10.6599 19.465 10.6392 19.4474C10.2641 19.1244 9.86566 18.781 9.57428 18.4519C9.24483 18.0797 8.83331 17.489 8.83331 16.6667C8.83331 15.8444 9.24483 15.2537 9.57428 14.8815C9.86566 14.5524 10.2642 14.2092 10.6392 13.8861C10.6599 13.8683 10.6804 13.8506 10.7009 13.8329L12.7452 12.0709C13.4424 11.47 14.4948 11.548 15.0957 12.2453Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M22.6942 10.086C23.5673 10.3771 24.0393 11.3209 23.7483 12.1942L20.415 22.1942C20.1238 23.0673 19.18 23.5393 18.3067 23.2483C17.4335 22.9572 16.9616 22.0133 17.2527 21.14L20.586 11.1401C20.877 10.2668 21.821 9.7949 22.6942 10.086Z" fill="#2EB79C"/>
                    <path d="M16.7132 31.6667C16.7779 32.2224 16.7569 32.7842 16.6585 33.3165C16.546 33.9249 16.4897 34.229 16.0264 34.6145C15.5631 35 15.1077 35 14.1969 35H12.1667C11.2462 35 10.5 35.7462 10.5 36.6667C10.5 37.5872 11.2462 38.3334 12.1667 38.3334H28.8333C29.7538 38.3334 30.5 37.5872 30.5 36.6667C30.5 35.7462 29.7538 35 28.8333 35H26.803C25.8922 35 25.4368 35 24.9735 34.6145C24.5102 34.229 24.454 33.9249 24.3415 33.3165C24.243 32.7842 24.222 32.2224 24.2867 31.6667C24.1682 31.6667 24.0487 31.6667 23.9278 31.6667H17.0721C16.9514 31.6667 16.8317 31.6667 16.7132 31.6667Z" fill="#2EB79C"/></svg>"""
        },
        {
            'id': 2, 'slug': 'business-management', 'discipline_name': 'Business & Management',
            'icons': """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path opacity="0.4" d="M11.2406 22.3074C9.20401 21.8759 7.45705 20.7557 6.33331 19.2122V22.5004C6.33331 28.7857 6.33331 31.9284 8.17746 33.8811C10.0216 35.8337 12.9897 35.8337 18.926 35.8337H22.074C28.0103 35.8337 30.9783 35.8337 32.8225 33.8811C34.6666 31.9284 34.6666 28.7857 34.6666 22.5004V19.2122C33.543 20.7557 31.796 21.8759 29.7593 22.3074C28.8481 22.5004 27.778 22.5004 25.6376 22.5004H23.8333V23.3334C23.8333 25.1744 22.341 26.6667 20.5 26.6667C18.659 26.6667 17.1666 25.1744 17.1666 23.3334V22.5004H15.3624C13.2219 22.5004 12.1517 22.5004 11.2406 22.3074Z" fill="#2EB79C"/>
                    <path d="M17.1667 22.2222C17.1667 21.7055 17.1667 21.4472 17.2235 21.2353C17.3775 20.6602 17.8269 20.2108 18.402 20.0568C18.6139 20 18.8722 20 19.3889 20H21.6112C22.1279 20 22.3862 20 22.598 20.0568C23.1732 20.2108 23.6225 20.6602 23.7765 21.2353C23.8334 21.4472 23.8334 21.7055 23.8334 22.2222V23.3333C23.8334 25.1743 22.341 26.6667 20.5 26.6667C18.659 26.6667 17.1667 25.1743 17.1667 23.3333V22.2222Z" stroke="#2EB79C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M23.6667 22.5H25.6377C27.778 22.5 28.8482 22.5 29.7593 22.307C32.3967 21.7483 34.5483 20.0345 35.4898 17.7425C35.8152 16.9506 35.9478 15.9925 36.2133 14.0761C36.313 13.3567 36.3628 12.997 36.315 12.7028C36.1753 11.8459 35.4887 11.1439 34.5635 10.9127C34.2459 10.8333 33.8442 10.8333 33.0407 10.8333H7.95938C7.15586 10.8333 6.7541 10.8333 6.43647 10.9127C5.51138 11.1439 4.82463 11.8459 4.68508 12.7028C4.63717 12.997 4.687 13.3567 4.78665 14.0761C5.05215 15.9925 5.18488 16.9506 5.51016 17.7425C6.45168 20.0345 8.60331 21.7483 11.2406 22.307C12.1518 22.5 13.222 22.5 15.3624 22.5H17.3333" stroke="#2EB79C" stroke-width="2.5"/>
                    <path d="M6.33331 19.1667V22.5C6.33331 28.7854 6.33331 31.9282 8.17746 33.8807C10.0216 35.8334 12.9897 35.8334 18.926 35.8334H22.074C28.0103 35.8334 30.9783 35.8334 32.8225 33.8807C34.6666 31.9282 34.6666 28.7854 34.6666 22.5V19.1667" stroke="#2EB79C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M26.3334 10.8334L26.2045 10.2447C25.5629 7.31124 25.242 5.84454 24.4782 5.0056C23.7144 4.16669 22.6999 4.16669 20.6705 4.16669H20.3295C18.3002 4.16669 17.2857 4.16669 16.5218 5.0056C15.758 5.84454 15.4372 7.31124 14.7955 10.2447L14.6667 10.8334" stroke="#2EB79C" stroke-width="2.5"/></svg>"""
        },
        {
            "id":3, 'slug': 'arts-design-architecture', 'discipline_name': 'Arts, Design & Architecture',
            'icons':"""<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M37.1667 20C37.1667 10.7952 29.7047 3.33331 20.5 3.33331C11.2953 3.33331 3.83334 10.7952 3.83334 20C3.83334 29.2046 11.2953 36.6666 20.5 36.6666C21.9028 36.6666 23.8333 36.8605 23.8333 35C23.8333 33.985 23.3053 33.202 22.781 32.424C22.0137 31.2858 21.2538 30.1588 22.1667 28.3333C23.2778 26.1111 25.1297 26.1111 27.9692 26.1111C29.389 26.1111 31.0557 26.1111 33 25.8333C36.5017 25.3331 37.1667 23.1806 37.1667 20Z" stroke="#2EB79C" stroke-width="2.5"/>
                    <path d="M12.1667 25.0034L12.1811 24.9994" stroke="#2EB79C" stroke-width="3.33333" stroke-linecap="round" stroke-linejoin="round"/>
                    <path opacity="0.4" d="M16.3333 16.6667C17.7141 16.6667 18.8333 15.5474 18.8333 14.1667C18.8333 12.786 17.7141 11.6667 16.3333 11.6667C14.9526 11.6667 13.8333 12.786 13.8333 14.1667C13.8333 15.5474 14.9526 16.6667 16.3333 16.6667Z" stroke="#2EB79C" stroke-width="2.5"/>
                    <path opacity="0.4" d="M28 18.3333C29.3807 18.3333 30.5 17.214 30.5 15.8333C30.5 14.4526 29.3807 13.3333 28 13.3333C26.6193 13.3333 25.5 14.4526 25.5 15.8333C25.5 17.214 26.6193 18.3333 28 18.3333Z" stroke="#2EB79C" stroke-width="2.5"/>
                    </svg>"""
        },
        {
            "id": 4, "slug": "agriculture-forestry", "discipline_name": "Agriculture & Forestry",
            "icons": """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M11.3333 18.75C6.50084 18.75 2.58333 22.6675 2.58333 27.5C2.58333 32.3325 6.50084 36.25 11.3333 36.25C16.1658 36.25 20.0833 32.3325 20.0833 27.5C20.0833 22.6675 16.1658 18.75 11.3333 18.75Z" fill="#2EB79C"/>
                    <path d="M33 25C29.7783 25 27.1667 27.6117 27.1667 30.8333C27.1667 34.055 29.7783 36.6667 33 36.6667C36.2217 36.6667 38.8333 34.055 38.8333 30.8333C38.8333 27.6117 36.2217 25 33 25Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M36.4965 18.75C36.8605 19.5148 37.0598 20.3483 37.176 21.25H34.0221C33.3318 21.25 32.7721 20.6903 32.7721 20C32.7721 19.3097 33.3318 18.75 34.0221 18.75H36.4965Z" fill="#2EB79C"/>
                    <path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M21.2855 4.60403C21.0667 3.70996 20.1643 3.16261 19.2703 3.38151C18.3763 3.60041 17.829 4.50265 18.0478 5.39671L20.2667 14.4595C20.2735 14.4872 20.281 14.5148 20.2892 14.5421C20.429 15.0082 20.5 15.4922 20.5 15.9788V16.6986C18.0302 14.6005 14.8303 13.3333 11.3334 13.3333C10.4806 13.3333 9.64512 13.4088 8.83334 13.5535V5.00036C8.83334 4.0799 8.08714 3.3337 7.16667 3.3337C6.24621 3.3337 5.50001 4.0799 5.50001 5.00036V14.5867C4.55031 15.0164 3.65641 15.5476 2.83247 16.1665C2.09649 16.7193 1.94801 17.764 2.50082 18.5C3.05364 19.236 4.09842 19.3845 4.83441 18.8316C6.64484 17.4718 8.89271 16.6666 11.3334 16.6666C15.4646 16.6666 19.0583 18.9785 20.887 22.3868C21.7032 23.9081 22.1668 25.6475 22.1668 27.5C22.1668 27.7273 22.159 27.9596 22.1513 28.1886C22.1387 28.5706 22.1263 28.9435 22.1507 29.268C22.246 30.5411 23.0902 31.4645 24.3647 31.6222L24.378 31.6238C24.7025 31.6628 24.8648 31.6823 24.9772 31.5815C25.0895 31.4808 25.0877 31.2926 25.0838 30.9165L25.0833 30.8333C25.0833 26.461 28.6277 22.9166 33 22.9166C34.1555 22.9166 35.2533 23.1641 36.243 23.6091C36.7725 23.8473 37.0372 23.9663 37.1912 23.862C37.3452 23.7576 37.3338 23.4906 37.3112 22.9563C37.2882 22.4158 37.2535 21.9155 37.2008 21.454C37.0393 20.0398 36.6922 18.7891 35.8565 17.705C35.012 16.6091 33.9065 15.9879 32.6057 15.5418C31.3818 15.1222 29.8283 14.8085 27.969 14.4332L23.4695 13.5246L21.2855 4.60403Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M3.83333 4.99998C3.83333 4.07951 4.57953 3.33331 5.49999 3.33331H22.1667C23.0872 3.33331 23.8333 4.07951 23.8333 4.99998C23.8333 5.92045 23.0872 6.66665 22.1667 6.66665H5.49999C4.57953 6.66665 3.83333 5.92045 3.83333 4.99998Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M12.1667 3.33331C13.0871 3.33331 13.8333 4.07951 13.8333 4.99998V13.5532C13.0219 13.4087 12.1865 13.3333 11.3334 13.3333C11.0537 13.3333 10.7758 13.3414 10.5 13.3575V4.99998C10.5 4.07951 11.2462 3.33331 12.1667 3.33331ZM32.1667 15.3999V13.3333C32.1667 12.4128 32.9128 11.6666 33.8333 11.6666C34.7538 11.6666 35.5 10.9204 35.5 9.99998C35.5 9.07951 34.7538 8.33331 33.8333 8.33331C31.0718 8.33331 28.8333 10.5719 28.8333 13.3333V14.6084C30.1102 14.8693 31.2243 15.1118 32.1667 15.3999Z" fill="#2EB79C"/>
                    </svg>"""
        },
        {
            "id": 5, "slug": "applied-science", "discipline_name": "Applied Sciences & Professions",
            "icons": """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path opacity="0.4" d="M7.70133 34.2546C9.18393 36.6676 12.9559 36.6676 20.5 36.6676C28.044 36.6676 31.816 36.6676 33.2987 34.2546L33.3213 34.2174C34.7827 31.7921 33.0013 28.5201 29.4388 21.9762L28.3635 20.0009C25.321 23.3342 21.8535 21.9454 20.5 20.8342C19.4755 19.8096 18.3808 19.1782 17.3512 18.8081C14.9704 17.9521 12.7708 19.7542 11.5611 21.9762C7.99863 28.5201 6.21741 31.7921 7.67875 34.2174L7.70133 34.2546Z" fill="#2EB79C"/>
                    <path d="M24.7342 3.33331V7.47701C24.7342 10.3903 24.7342 11.8469 25.0908 13.2452C25.4475 14.6436 26.1465 15.9275 27.5445 18.4955L29.4388 21.9753C33.0013 28.5191 34.7827 31.7911 33.3213 34.2166L33.2987 34.2536C31.816 36.6666 28.044 36.6666 20.5 36.6666C12.9559 36.6666 9.18393 36.6666 7.70133 34.2536L7.67875 34.2166C6.21741 31.7911 7.99863 28.5191 11.5611 21.9753L13.4555 18.4955C14.8535 15.9275 15.5525 14.6436 15.9091 13.2452C16.2658 11.8469 16.2658 10.3903 16.2658 7.47701V3.33331" stroke="#2EB79C" stroke-width="2.5"/>
                    <path d="M15.5 26.6701L15.5145 26.6661" stroke="#2EB79C" stroke-width="3.33333" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M25.5 30.0034L25.5145 29.9994" stroke="#2EB79C" stroke-width="3.33333" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M13.8333 3.33331H27.1667" stroke="#2EB79C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M13 19.2606C14.6667 17.3383 17.3323 18.7239 20.5 20.5304C24.6667 22.9066 27.1667 21.0834 28 19.3588" stroke="#2EB79C" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>"""
        },
        {
            "id": 6, "slug": "education-training", "discipline_name": "Education & Training",
            "icons": """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M21.4273 2.08331H19.5727C16.5097 2.0833 14.0837 2.08326 12.185 2.33855C10.2309 2.60125 8.64936 3.15478 7.40208 4.40205C6.15481 5.64933 5.60128 7.23091 5.33858 9.18495C5.08329 11.0836 5.08331 13.5097 5.08334 16.5726V32.2211C5.07903 32.3136 5.07683 32.4065 5.07683 32.5C5.07683 35.6986 7.63868 38.3333 10.8498 38.3333H34.2333C34.2332 38.3333 34.2335 38.3333 34.2333 38.3333C34.2405 38.3333 34.2478 38.3333 34.2548 38.3331C34.2783 38.3328 34.3018 38.3321 34.3252 38.3308C35.2032 38.2833 35.9003 37.5565 35.9003 36.6666C35.9003 35.7461 35.1542 35 34.2337 35C32.853 35 31.7337 33.8806 31.7337 32.5C31.7337 31.1193 32.853 30 34.2337 30C35.0195 30 35.6782 29.4563 35.8542 28.7246C35.8947 28.6015 35.9167 28.47 35.9167 28.3333V16.5726C35.9167 13.5097 35.9167 11.0836 35.6615 9.18495C35.3987 7.23091 34.8452 5.64933 33.598 4.40205C32.3507 3.15478 30.769 2.60125 28.815 2.33855C26.9163 2.08326 24.4903 2.0833 21.4273 2.08331ZM28.9618 30H10.8498C9.52528 30 8.41016 31.0963 8.41016 32.5C8.41016 33.9036 9.52528 35 10.8498 35H28.9618C28.6018 34.2423 28.4003 33.3946 28.4003 32.5C28.4003 31.6053 28.6018 30.7576 28.9618 30Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M26.75 11.6667C26.75 12.357 26.1903 12.9167 25.5 12.9167H15.5C14.8097 12.9167 14.25 12.357 14.25 11.6667C14.25 10.9763 14.8097 10.4167 15.5 10.4167H25.5C26.1903 10.4167 26.75 10.9763 26.75 11.6667Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M21.75 18.3333C21.75 19.0236 21.1903 19.5833 20.5 19.5833H15.5C14.8097 19.5833 14.25 19.0236 14.25 18.3333C14.25 17.643 14.8097 17.0833 15.5 17.0833H20.5C21.1903 17.0833 21.75 17.643 21.75 18.3333Z" fill="#2EB79C"/>
                    </svg>"""
        },
        {
            "id": 7, "slug": "engineering-technology", "discipline_name": "Engineering & Technology",
            "icons": """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path opacity="0.4" d="M8.83331 26.6666L17.1666 21.6666M23.8333 18.3333L32.1666 13.3333M20.5 8.33331V16.6666M20.5 23.3333V31.6666M8.83331 13.3333L17.1666 18.3333M23.8333 21.6666L32.1666 26.6666" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    <path opacity="0.4" d="M34.6666 15V24.1666M23 34.1666L32.1666 29.1666M7.99998 29.1666L18 34.1666M6.33331 25V15M7.99998 10.8333L18 5.83331M33 10.8333L23 5.83331" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    <path d="M20.5 8.33331C21.8807 8.33331 23 7.21402 23 5.83331C23 4.4526 21.8807 3.33331 20.5 3.33331C19.1193 3.33331 18 4.4526 18 5.83331C18 7.21402 19.1193 8.33331 20.5 8.33331Z" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    <path d="M20.5 36.6667C21.8807 36.6667 23 35.5474 23 34.1667C23 32.786 21.8807 31.6667 20.5 31.6667C19.1193 31.6667 18 32.786 18 34.1667C18 35.5474 19.1193 36.6667 20.5 36.6667Z" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    <path d="M6.33331 15C7.71402 15 8.83331 13.8807 8.83331 12.5C8.83331 11.1193 7.71402 10 6.33331 10C4.9526 10 3.83331 11.1193 3.83331 12.5C3.83331 13.8807 4.9526 15 6.33331 15Z" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    <path d="M34.6667 15C36.0474 15 37.1667 13.8807 37.1667 12.5C37.1667 11.1193 36.0474 10 34.6667 10C33.286 10 32.1667 11.1193 32.1667 12.5C32.1667 13.8807 33.286 15 34.6667 15Z" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    <path d="M34.6667 30C36.0474 30 37.1667 28.8807 37.1667 27.5C37.1667 26.1193 36.0474 25 34.6667 25C33.286 25 32.1667 26.1193 32.1667 27.5C32.1667 28.8807 33.286 30 34.6667 30Z" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    <path d="M6.33331 30C7.71402 30 8.83331 28.8807 8.83331 27.5C8.83331 26.1193 7.71402 25 6.33331 25C4.9526 25 3.83331 26.1193 3.83331 27.5C3.83331 28.8807 4.9526 30 6.33331 30Z" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    <path d="M20.5 16.25L23.8334 18.125V21.875L20.5 23.75L17.1667 21.875V18.125L20.5 16.25Z" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    </svg>"""
        },
        {
             "id": 8, "slug": "health-medicine", "discipline_name": "Health & Medicine",
            "icons": """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path opacity="0.4" d="M25.5878 8.95831C28.2631 8.9583 30.3903 8.95826 32.057 9.16835C33.7701 9.38426 35.1855 9.84103 36.313 10.8981C37.452 11.966 37.9548 13.3245 38.1905 14.9677C38.4166 16.5456 38.4166 18.5531 38.4166 21.0481V24.3685C38.4166 26.8635 38.4166 28.871 38.1905 30.449C37.9548 32.0921 37.452 33.4506 36.313 34.5185C35.1855 35.5756 33.7701 36.0323 32.057 36.2483C30.3903 36.4583 28.2631 36.4583 25.5878 36.4583H15.4122C12.7368 36.4583 10.6096 36.4583 8.94291 36.2483C7.22988 36.0323 5.81453 35.5756 4.68693 34.5185C3.54791 33.4506 3.0452 32.0921 2.80955 30.449C2.58325 28.871 2.58328 26.8635 2.58331 24.3685V21.0481C2.58328 18.5531 2.58325 16.5456 2.80955 14.9677C3.0452 13.3245 3.54791 11.966 4.68693 10.8981C5.81453 9.84103 7.22988 9.38426 8.94291 9.16835C10.6096 8.95826 12.7368 8.9583 15.4122 8.95831H25.5878Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M20.5 16.0417C21.4205 16.0417 22.1666 16.7879 22.1666 17.7084V21.0417H25.5C26.4205 21.0417 27.1666 21.7879 27.1666 22.7084C27.1666 23.6289 26.4205 24.375 25.5 24.375H22.1666V27.7084C22.1666 28.6289 21.4205 29.375 20.5 29.375C19.5795 29.375 18.8333 28.6289 18.8333 27.7084V24.375H15.5C14.5795 24.375 13.8333 23.6289 13.8333 22.7084C13.8333 21.7879 14.5795 21.0417 15.5 21.0417H18.8333V17.7084C18.8333 16.7879 19.5795 16.0417 20.5 16.0417Z" fill="#2EB79C"/>
                    <path d="M13.8703 8.96002C13.8971 8.59012 13.938 8.28827 13.9926 8.03955C14.0949 7.5739 14.2215 7.40667 14.2925 7.33562C14.3636 7.26455 14.5308 7.13804 14.9965 7.03574C15.481 6.92929 16.1672 6.87502 17.1653 6.87502H23.8319C24.83 6.87502 25.5162 6.92929 26.0007 7.03574C26.4664 7.13804 26.6335 7.26455 26.7047 7.33562C26.7757 7.40667 26.9022 7.5739 27.0045 8.03955C27.0592 8.28827 27.1 8.59012 27.1269 8.96002C28.3744 8.96427 29.4852 8.97934 30.4712 9.03262C30.4389 8.41792 30.3749 7.8457 30.2602 7.32434C30.0714 6.46469 29.7235 5.64045 29.0617 4.97859C28.3999 4.31674 27.5755 3.96889 26.716 3.78004C25.8752 3.59534 24.9022 3.54169 23.8319 3.54169H17.1653C16.095 3.54169 15.122 3.59534 14.2812 3.78004C13.4216 3.96889 12.5974 4.31674 11.9355 4.97859C11.2736 5.64045 10.9258 6.46469 10.7369 7.32434C10.6224 7.8457 10.5583 8.41792 10.5261 9.03262C11.5119 8.97934 12.6228 8.96427 13.8703 8.96002Z" fill="#2EB79C"/>
                    </svg>"""
        },
        {
            "id": 9, "slug": "environmental-studies", "discipline_name": "Environmental Studies",
            "icons": """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path opacity="0.4" d="M20.5 36.6666C11.2953 36.6666 3.83334 29.2046 3.83334 20C3.83334 15.3457 5.74109 11.1371 8.81729 8.11333C10.2328 8.26271 11.0253 9.02103 12.3416 10.4119C14.8407 13.0525 17.3397 13.2728 19.0058 12.3926C21.5048 11.0723 19.4048 8.9338 22.3378 7.7716C24.136 7.05915 24.4787 5.19328 23.6277 3.62628C31.3373 5.09005 37.1667 11.8642 37.1667 20C37.1667 20.9616 37.0852 21.9045 36.9288 22.8216C33.4568 21.6015 31.5078 25.2968 28.8333 24.7618C22.881 23.5713 21.1943 24.9021 21.1943 27.7406C21.1943 30.579 21.1943 30.579 19.9563 32.7078C19.1512 34.0925 18.895 35.4771 20.5 36.6666Z" fill="#2EB79C"/>
                    <path d="M20.5 36.6666C11.2953 36.6666 3.83334 29.2046 3.83334 20C3.83334 15.3457 5.74109 11.1371 8.81729 8.11335M20.5 36.6666C18.895 35.4773 19.1512 34.0925 19.9563 32.7078C21.1943 30.579 21.1943 30.579 21.1943 27.7406C21.1943 24.9023 22.881 23.5715 28.8333 24.7618C31.5078 25.2968 33.4568 21.6015 36.9288 22.8216M20.5 36.6666C28.743 36.6666 35.5883 30.6826 36.9288 22.8216M8.81729 8.11335C10.2328 8.26273 11.0253 9.02105 12.3416 10.4119C14.8407 13.0525 17.3397 13.2728 19.0058 12.3926C21.5048 11.0724 19.4048 8.93381 22.3378 7.77161C24.136 7.05916 24.4787 5.1933 23.6277 3.6263M8.81729 8.11335C11.8249 5.157 15.9495 3.33331 20.5 3.33331C21.569 3.33331 22.6145 3.43396 23.6277 3.6263M36.9288 22.8216C37.0852 21.9045 37.1667 20.9618 37.1667 20C37.1667 11.8643 31.3373 5.09006 23.6277 3.6263" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    </svg>"""
        },
        {
            "id": 10, "slug": "social-sciences", "discipline_name": "Social Sciences",
            "icons": """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M13.4167 7.5C13.4167 9.57107 11.7377 11.25 9.66667 11.25C7.59561 11.25 5.91667 9.57107 5.91667 7.5C5.91667 5.42893 7.59561 3.75 9.66667 3.75C11.7377 3.75 13.4167 5.42893 13.4167 7.5Z" fill="#2EB79C"/>
                    <path d="M35.0833 7.5C35.0833 9.57107 33.4043 11.25 31.3333 11.25C29.2623 11.25 27.5833 9.57107 27.5833 7.5C27.5833 5.42893 29.2623 3.75 31.3333 3.75C33.4043 3.75 35.0833 5.42893 35.0833 7.5Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M15.9167 10C15.9167 9.30965 16.4763 8.75 17.1667 8.75H18C18.6903 8.75 19.25 9.30965 19.25 10C19.25 10.6903 18.6903 11.25 18 11.25H17.1667C16.4763 11.25 15.9167 10.6903 15.9167 10Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M21.75 10C21.75 9.30965 22.3097 8.75 23 8.75H23.8333C24.5237 8.75 25.0833 9.30965 25.0833 10C25.0833 10.6903 24.5237 11.25 23.8333 11.25H23C22.3097 11.25 21.75 10.6903 21.75 10Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M6.33342 22.0833C7.02377 22.0833 7.58342 22.643 7.58342 23.3333V28.3333C7.58342 29.1676 7.58946 29.4023 7.62345 29.5731C7.78783 30.3995 8.43386 31.0455 9.2603 31.21C9.43111 31.244 9.66573 31.25 10.5001 31.25C11.1904 31.25 11.7501 31.8096 11.7501 32.5C11.7501 33.1903 11.1904 33.75 10.5001 33.75C10.4588 33.75 10.4181 33.75 10.3779 33.75C9.72342 33.7503 9.21842 33.7506 8.77258 33.662C6.95442 33.3003 5.53313 31.879 5.17148 30.0608C5.0828 29.615 5.08305 29.11 5.08337 28.4555C5.0834 28.4153 5.08342 28.3746 5.08342 28.3333V23.3333C5.08342 22.643 5.64305 22.0833 6.33342 22.0833ZM34.6667 22.0833C35.3572 22.0833 35.9167 22.643 35.9167 23.3333V28.3333C35.9167 28.3746 35.9168 28.4153 35.9168 28.4555C35.9172 29.11 35.9173 29.615 35.8287 30.0608C35.467 31.879 34.0457 33.3003 32.2275 33.662C31.7817 33.7506 31.2767 33.7503 30.6222 33.75C30.582 33.75 30.5413 33.75 30.5 33.75C29.8097 33.75 29.25 33.1903 29.25 32.5C29.25 31.8096 29.8097 31.25 30.5 31.25C31.3345 31.25 31.569 31.244 31.7398 31.21C32.5663 31.0455 33.2123 30.3995 33.3767 29.5731C33.4107 29.4023 33.4167 29.1676 33.4167 28.3333V23.3333C33.4167 22.643 33.9763 22.0833 34.6667 22.0833Z" fill="#2EB79C"/>
                    <path d="M13.804 14.0086C14.2512 14.2505 15.2978 14.8184 15.861 15.35C16.2097 15.6792 16.6541 16.2125 16.7371 16.9448C16.8297 17.7617 16.4405 18.4489 15.8841 18.96C15.0511 19.7254 13.9651 20.4167 12.5248 20.4167H6.80927C5.369 20.4167 4.283 19.7254 3.44995 18.96C2.89357 18.4489 2.50438 17.7617 2.59697 16.9448C2.67998 16.2125 3.12432 15.6792 3.47305 15.35C4.03625 14.8184 5.08287 14.2505 5.53008 14.0086C8.06582 12.5527 11.2682 12.5527 13.804 14.0086Z" fill="#2EB79C"/>
                    <path d="M35.4707 14.0086C35.9178 14.2505 36.9645 14.8184 37.5277 15.35C37.8763 15.6792 38.3207 16.2125 38.4038 16.9448C38.4963 17.7617 38.1072 18.4489 37.5508 18.96C36.7177 19.7254 35.6317 20.4167 34.1915 20.4167H28.476C27.0357 20.4167 25.9497 19.7254 25.1167 18.96C24.5602 18.4489 24.171 17.7617 24.2637 16.9448C24.3467 16.2125 24.791 15.6792 25.1397 15.35C25.703 14.8184 26.7495 14.2505 27.1967 14.0086C29.7325 12.5527 32.9348 12.5527 35.4707 14.0086Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M24.25 27.167V25.8333C24.25 23.7623 22.571 22.0833 20.5 22.0833C18.429 22.0833 16.75 23.7623 16.75 25.8333V27.167C16.1583 27.2596 15.5761 27.4658 15.1043 27.9376C14.5893 28.4526 14.4018 29.0788 14.3222 29.6713C14.2499 30.2093 14.2499 31.0198 14.25 31.7411C14.2499 32.4626 14.2499 33.124 14.3222 33.662C14.4018 34.2545 14.5893 34.8806 15.1043 35.3956C15.6193 35.9108 16.2455 36.0981 16.838 36.1778C17.376 36.2501 18.0373 36.2501 18.7587 36.25H22.2413C22.9627 36.2501 23.624 36.2501 24.162 36.1778C24.7545 36.0981 25.3807 35.9108 25.8957 35.3956C26.4108 34.8806 26.5982 34.2545 26.6778 33.662C26.7502 33.124 26.7502 32.4626 26.75 31.7413C26.7502 31.0198 26.7502 30.2093 26.6778 29.6713C26.5982 29.0788 26.4108 28.4526 25.8957 27.9376C25.424 27.4658 24.8417 27.2596 24.25 27.167ZM19.25 25.8333C19.25 25.143 19.8097 24.5833 20.5 24.5833C21.1903 24.5833 21.75 25.143 21.75 25.8333V27.0833H19.25V25.8333Z" fill="#2EB79C"/>
                    </svg>"""
        },
        {
            "id": 11, "slug": "journalism-media", "discipline_name": "Journalism & Media",
            "icons": """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path opacity="0.4" d="M10.9167 11.6666C10.9167 6.37391 15.2073 2.08331 20.5 2.08331C25.7927 2.08331 30.0833 6.37391 30.0833 11.6666V18.3333C30.0833 23.626 25.7927 27.9166 20.5 27.9166C15.2073 27.9166 10.9167 23.626 10.9167 18.3333V11.6666Z" fill="#2EB79C"/>
                    <path d="M30.0833 17.0833V18.3333C30.0833 18.757 30.0558 19.1741 30.0025 19.5833H23.8333C23.143 19.5833 22.5833 19.0236 22.5833 18.3333C22.5833 17.643 23.143 17.0833 23.8333 17.0833H30.0833Z" fill="#2EB79C"/>
                    <path d="M30.0025 10.4167C30.0558 10.8258 30.0833 11.243 30.0833 11.6667V12.9167H23.8333C23.143 12.9167 22.5833 12.357 22.5833 11.6667C22.5833 10.9763 23.143 10.4167 23.8333 10.4167H30.0025Z" fill="#2EB79C"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M7.53703 17.0833C8.43195 17.0833 9.1574 17.8008 9.1574 18.6858C9.1574 24.8813 14.2357 29.9038 20.5 29.9038C26.7643 29.9038 31.8427 24.8813 31.8427 18.6858C31.8427 17.8008 32.568 17.0833 33.463 17.0833C34.3578 17.0833 35.0833 17.8008 35.0833 18.6858C35.0833 26.1098 29.412 32.2238 22.1203 33.021V34.7115H25.3612C26.256 34.7115 26.9815 35.429 26.9815 36.3141C26.9815 37.1991 26.256 37.9166 25.3612 37.9166H15.6389C14.744 37.9166 14.0185 37.1991 14.0185 36.3141C14.0185 35.429 14.744 34.7115 15.6389 34.7115H18.8797V33.021C11.5881 32.2238 5.91667 26.1098 5.91667 18.6858C5.91667 17.8008 6.64213 17.0833 7.53703 17.0833Z" fill="#2EB79C"/>
                    </svg>"""
        },
        {
            "id": 12, "slug": "law", "discipline_name": "Law",
            "icons": """<svg width="41" height="40" viewBox="0 0 41 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4.41898 22.0225C3.83061 18.1936 3.53643 16.2794 4.26028 14.5823C4.98411 12.8852 6.59004 11.724 9.80189 9.40175L12.2016 7.66665C16.1971 4.77776 18.1948 3.33331 20.5 3.33331C22.8052 3.33331 24.8028 4.77776 28.7983 7.66665L31.1982 9.40175C34.41 11.724 36.0158 12.8852 36.7397 14.5823C37.4635 16.2794 37.1693 18.1936 36.581 22.0225L36.0793 25.2873C35.2452 30.7148 34.8282 33.4286 32.8817 35.0476C30.9352 36.6666 28.0895 36.6666 22.398 36.6666H18.602C12.9105 36.6666 10.0648 36.6666 8.11833 35.0476C6.17181 33.4286 5.75478 30.7148 4.92071 25.2873L4.41898 22.0225Z" stroke="#2EB79C" stroke-width="2.5" stroke-linejoin="round"/>
                    <path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M4.26028 14.5823C3.53643 16.2794 3.83061 18.1936 4.41898 22.0225L4.92071 25.2873C5.75478 30.7148 6.17181 33.4286 8.11833 35.0476C10.0648 36.6666 12.9105 36.6666 18.602 36.6666H22.398C28.0895 36.6666 30.9352 36.6666 32.8817 35.0476C34.8282 33.4286 35.2452 30.7148 36.0793 25.2873L36.581 22.0225C37.1693 18.1936 37.4635 16.2794 36.7397 14.5823C36.0158 12.8852 34.41 11.724 31.1982 9.40175L28.7983 7.66665C24.8028 4.77776 22.8052 3.33331 20.5 3.33331C18.1948 3.33331 16.1971 4.77776 12.2016 7.66665L9.80189 9.40175C6.59004 11.724 4.98411 12.8852 4.26028 14.5823ZM23.4167 17.9166C21.4387 15.9386 18.8333 13.9285 18.8333 13.9285L15.2619 17.5C15.2619 17.5 17.272 20.1053 19.25 22.0833C21.228 24.0613 23.8333 26.0715 23.8333 26.0715L27.4048 22.5C27.4048 22.5 25.3947 19.8946 23.4167 17.9166Z" fill="#2EB79C"/>
                    <path d="M19.25 22.0833C21.228 24.0613 23.8333 26.0715 23.8333 26.0715L27.4048 22.5C27.4048 22.5 25.3947 19.8946 23.4167 17.9166C21.4387 15.9386 18.8333 13.9285 18.8333 13.9285L15.2619 17.5C15.2619 17.5 17.272 20.1053 19.25 22.0833ZM19.25 22.0833L13 28.3333M28 21.9048L23.2382 26.6666M19.4285 13.3333L14.6667 18.0951" stroke="#2EB79C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>"""
        }
    ]
    
    seed_model(db, DisciplineModel, data)